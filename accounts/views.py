import pyotp
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect
from config import settings
from .forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib import messages
from .models import UserOTP
from django.http import HttpResponseForbidden, FileResponse
import os
from django.core.exceptions import PermissionDenied
import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)
User = get_user_model()

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            request.session["pre_otp_user_id"] = user.id
            generate_otp(user)
            return redirect('otp_verify')
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def home_view(request):
    return render(request, 'accounts/home.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    return Response({'username': request.user.username, 'email': request.user.email})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def generate_otp(user):
    otp_obj, created = UserOTP.objects.get_or_create(user=user)
    if not otp_obj.secret:
        otp_obj.secret = pyotp.random_base32()
        otp_obj.save()
    totp = pyotp.TOTP(otp_obj.secret, interval=30)
    otp_code = totp.now()
    print(f"🔑 OTP برای {user.username}: {otp_code}")
    return otp_code


def otp_verify(request):
    try:
        user_id = request.session.get("pre_otp_user_id")
        if not user_id:
            return redirect("login")

        user = User.objects.get(id=user_id)
        otp_obj = UserOTP.objects.get(user=user)
        totp = pyotp.TOTP(otp_obj.secret, interval=30)

        if request.method == 'POST':
            code = request.POST['otp']

            if totp.verify(code, valid_window=1):
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                request.session.pop("pre_otp_user_id", None)
                return redirect('home')
            else:
                return render(request, 'accounts/otp_verify.html', {'error': 'کد اشتباه یا منقضی شده است'})

        return render(request, "accounts/otp_verify.html")

    except User.DoesNotExist:
        return render(request, "error.html", {"error": "کاربر یافت نشد"})
    except Exception as e:
        logger.error(f"❌ خطا در OTP Verify: {e}")
        return render(request, "error.html", {"error": "خطای غیرمنتظره‌ای رخ داد"})

def manager_panel(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.groups.filter(name='Managers').exists():
        return render(request, 'accounts/manager_panel.html')

    raise PermissionDenied


@login_required
def secure_download(request, filename):
    try:
        if not request.user.is_superuser:
            return HttpResponseForbidden("Access denied")

        filepath = os.path.join(settings.MEDIA_ROOT, 'sensitive', filename)
        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)

    except FileNotFoundError:
        return render(request, "error.html", {"error": "فایل پیدا نشد"})
    except Exception as e:
        logger.error(f"❌ خطا در دانلود فایل {filename}: {e}")
        return render(request, "error.html", {"error": "خطای غیرمنتظره‌ای رخ داد"})


def crash(request):
    1 / 0  # خطای عمدی برای تست
    return HttpResponse("این خط هرگز اجرا نمی‌شود!")
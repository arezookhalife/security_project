import pyotp
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect
from .forms import LoginForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib import messages
from .models import UserOTP

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            request.session["pre_otp_user_id"] = user.id
            otp_obj, created = UserOTP.objects.get_or_create(user=user)
            if created:
                otp_obj.secret = pyotp.random_base32()
                otp_obj.save()
            totp = pyotp.TOTP(otp_obj.secret, interval=60)
            otp_code = totp.now()
            print(f"🔑 OTP برای {user.username}: {otp_code}")
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
    totp = pyotp.TOTP(otp_obj.secret)
    print("کد OTP فعلی:", totp.now())
    return totp.now()


def otp_verify(request):
    user_id = request.session.get("pre_otp_user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)
    otp_obj = UserOTP.objects.get(user=user)
    totp = pyotp.TOTP(otp_obj.secret, interval=60)

    if request.method == 'POST':
        code = request.POST['otp']

        if totp.verify(code):
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            del request.session["pre_otp_user_id"]
            return redirect('home')
        else:
            return render(request, 'accounts/otp_verify.html', {'error': 'کد اشتباه است'})

    otp_code = totp.now()
    print(f"🔄 کد جدید OTP برای {user.username}: {otp_code}")

    return render(request, "accounts/otp_verify.html")
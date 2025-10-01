from django.urls import path
from .views import login_view, home_view, logout_view, profile_api, otp_verify, register, manager_panel, crash, \
    test_login_no_otp

urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('api/profile/', profile_api, name='profile_api'),
    path('register/', register, name='register'),
    path('otp-verify/', otp_verify, name='otp_verify'),
    path('manager-panel/', manager_panel, name='manager_panel'),
    path("crash/", crash, name="crash"),
    path("test-login-no-otp/", test_login_no_otp, name="test_login_no_otp"),
]

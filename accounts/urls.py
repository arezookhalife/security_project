from django.urls import path
from .views import login_view, home_view, logout_view, profile_api

urlpatterns = [
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('api/profile/', profile_api, name='profile_api'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('login_signup/', views.signup_or_login, name='signup_or_login'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('complete_profile/', views.complete_profile, name='complete_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('update-profile/', views.update_profile, name='profile')
]
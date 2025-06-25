from django.urls import path
from .views import OTPViewSet
from users.Profile.views import ProfileViewSet, AuthViewSet, RegisterViewSet, UpdateProfileViewSet

urlpatterns = [
    path('otp-create/', OTPViewSet.as_view({'post': 'request_otp'}), name='otp-create'),
    path('otp-verify/', OTPViewSet.as_view({'post': 'verify_otp'}), name='otp-verify'),
    path('register/', RegisterViewSet.as_view({'post': 'register'}), name='auth-register'),
    path('login/', AuthViewSet.as_view({'post': 'login'}, name='auth-login')),
    path('change-password/', AuthViewSet.as_view({'post': 'change_password'}), name='auth-change-password'),
    path('profile/', UpdateProfileViewSet.as_view({'get': 'profile', 'patch': 'update_profile'}), name='auth-profile'),
    path('profiles/', ProfileViewSet.as_view({'get': 'list_profile'}), name='auth-profiles')
]
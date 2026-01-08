from django.http import JsonResponse
from django.urls import path

from logi_go_app.views.auth import auth_views

def api_info(request):
    return JsonResponse({"version": "1.0.0"})

urlpatterns = [
    path('info', api_info),
    path('signup', auth_views.SignupView.as_view(), name="signup"),
    path('otp-verify', auth_views.OtpVerifyView.as_view(), name="otp-verify"),
    path('set-password', auth_views.SetPasswordView.as_view(), name="otp-verify"),
    path('login', auth_views.LoginView.as_view(), name='login'),
]
import json
from django.views import View
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib.auth.hashers import make_password

import jwt

from logi_go_app.utils.jwt import generate_jwt_pair
from logi_go_app.utils.otp import generate_otp
from logi_go_app.utils.response import api_response


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            email = body.get("email")

            if not email:
                return api_response(False, "Email is required", status=400)

            otp = generate_otp()
            cache_key = f"signup_otp:{email}"
            cache.set(cache_key, otp, timeout=60 * 15)

            try:
                user = User.objects.create(
                    username=email,
                    email=email,
                    is_active=False 
                )
            except Exception as e:
                print("Unable to create user", e)

            try:
                html_content = render_to_string("emails/auth/otp.html", {"otp": otp})
                msg = EmailMultiAlternatives(
                    subject="Verify your email",
                    body=f"Your OTP is {otp}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as e:
                print("Unable to send OTP right now", e)

            print("For Testing Purposes, Your otp is here", otp)
            return api_response(
                True,
                "OTP sent to email",
                {
                    "email": email,
                    "is_active": False
                },
                status=200,
            )

        except Exception as e:
            print("Error @ Signup", e)
            return api_response(False, "Something went wrong", status=500)

class LoginView(View):
    pass


@method_decorator(csrf_exempt, name='dispatch')
class OtpVerifyView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            email = body.get("email")
            otp = body.get("otp")

            if not email or not otp:
                return api_response(
                    False,
                    "Email and OTP are required",
                    status=400,
                )

            cache_key = f"signup_otp:{email}"
            cached_otp = cache.get(cache_key)

            if not cached_otp:
                return api_response(
                    False,
                    "OTP expired or invalid",
                    status=400,
                )

            if otp != cached_otp:
                return api_response(
                    False,
                    "Incorrect OTP",
                    status=401,
                )

            user = User.objects.filter(email__iexact=email).first()

            if user:
                user.is_active = True
                user.save()

                cache.delete(cache_key)

                access_token, refresh_token = generate_jwt_pair(user)

                return api_response(
                    True,
                    "Signup successful",
                    {
                        "id": user.id,
                        "email": user.email,
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    },
                    status=201,
                )
            

        except Exception:
            return api_response(
                False,
                "Something went wrong",
                status=500,
            )

@method_decorator(csrf_exempt, name="dispatch")
class SetPasswordView(View):
    def post(self, request):
        try:
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return api_response(False, "Authorization token missing", status=401)

            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=["HS256"],
                )
            except jwt.ExpiredSignatureError:
                return api_response(False, "Token expired", status=401)
            except jwt.InvalidTokenError:
                return api_response(False, "Invalid token", status=401)

            body = json.loads(request.body)
            email = body.get("email")
            password = body.get("password")

            if not email or not password:
                return api_response(False, "Email and password are required", status=400)

            if payload.get("email") != email:
                return api_response(False, "Token email mismatch", status=403)

            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                return api_response(False, "User not found", status=404)
            
            if not user.is_active:
                return api_response(False, "Please verify your email first", status=404)


            user.password = make_password(password)
            user.is_active = True
            user.save(update_fields=["password", "is_active"])

            return api_response(
                True,
                "Password set successfully",
                {
                    "id": user.id,
                    "email": user.email,
                },
                status=200,
            )

        except Exception:
            return api_response(False, "Something went wrong", status=500)
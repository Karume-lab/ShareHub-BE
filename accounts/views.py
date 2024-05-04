from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework import status
from django.conf import settings
from rest_framework.views import APIView


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data["access"]
            refresh_token = response.data["refresh"]

            response.set_cookie(
                key=settings.AUTH_COOKIE,
                value=access_token,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
            )

            response.set_cookie(
                key=settings.AUTH_COOKIE_REFRESH,
                value=refresh_token,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get(settings.AUTH_COOKIE_REFRESH)

        if refresh_token:
            request.data["refresh"] = refresh_token

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data["access"]

            response.set_cookie(
                key=settings.AUTH_COOKIE,
                value=access_token,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                secure=settings.AUTH_COOKIE_SECURE,
                samesite=settings.AUTH_COOKIE_SAMESITE,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
            )
        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        access_token = request.COOKIES.get(settings.AUTH_COOKIE)

        if access_token:
            request.data["token"] = access_token

        response = super().post(request, *args, **kwargs)
        return response


class LogoutView(APIView):
    def post(self, request: Request) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(settings.AUTH_COOKIE)
        response.delete_cookie(settings.AUTH_COOKIE_REFRESH)
        return response

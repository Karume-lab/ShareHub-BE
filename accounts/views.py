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
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from . import serializers


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


@api_view(["GET", "POST"])
def user_profile_list(request):
    """
    List all user profiles or create a new user profile
    """
    if request.method == "GET":
        profiles = UserProfile.objects.all()
        serializer = serializers.UserProfile(profiles, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        data = request.data
        data["user"] = request.user.id
        serializer = serializers.UserProfile(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def user_profile_detail(request, pk):
    """
    Retrieve, update, or delete a user profile instance
    """
    try:
        profile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = serializers.UserProfile(profile)
        return Response(serializer.data)

    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = serializers.UserProfile(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = serializers.UserProfile(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return Response(
                {"detail": "User not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

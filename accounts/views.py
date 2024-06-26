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
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from core import models as core_models
from core import serializers as core_serializers
from utils import main


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
@permission_classes([AllowAny])
def user_profile_list(request):
    """
    List all user profiles
    """
    if request.method == "GET":
        profiles = models.UserProfile.objects.all()
        paginated_response = main.paginate(request, profiles, serializers.UserProfile)
        return paginated_response


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([AllowAny])
def user_profile_detail(request, pk):
    """
    Retrieve, update, or delete a user profile instance
    """
    try:
        profile = models.UserProfile.objects.get(pk=pk)
    except models.UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = serializers.UserProfile(profile, context={"request": request})
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not (
        request.user.is_staff
        or request.user.is_site_mod
        or request.user.user_profile == profile
    ):
        return Response(
            {"detail": "You do not have permission to access this resource."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method in ["PUT", "PATCH"]:
        serializer = serializers.UserProfile(
            profile,
            data=request.data,
            partial=request.method == "PATCH",
            context={"request": request},
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_user_profile(request):
    if request.method == "GET":
        try:
            profile = models.UserProfile.objects.get(user=request.user)
        except models.UserProfile.DoesNotExist:
            return Response(
                {"detail": "User profile does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = serializers.UserProfile(profile, context={"request": request})
        return Response(serializer.data)
    return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_innovation_list(request, pk):
    try:
        user = models.UserProfile.objects.get(pk=pk)
    except models.UserProfile.DoesNotExist:
        return Response(
            {"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    innovations = core_models.Innovation.objects.filter(author__user=user)
    paginated_response = main.paginate(
        request, innovations, core_serializers.Innovation
    )
    return paginated_response


@api_view(["GET"])
def user_bookmark_list(request, pk):
    try:
        user = models.UserProfile.objects.get(pk=pk)
    except models.UserProfile.DoesNotExist:
        return Response(
            {"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    bookmarks = core_models.Bookmark.objects.filter(user=user)
    paginated_response = main.paginate(request, bookmarks, core_serializers.Bookmark)
    return paginated_response


@api_view(["GET"])
def user_like_list(request, pk):
    try:
        user = models.UserProfile.objects.get(pk=pk)
    except models.UserProfile.DoesNotExist:
        return Response(
            {"detail": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
        )
    likes = core_models.Like.objects.filter(user=user)
    print(likes)
    paginated_response = main.paginate(request, likes, core_serializers.Like)
    return paginated_response


@api_view(["GET"])
def user_innovations(request):
    innovations = core_models.Innovation.objects.filter(
        author=request.user.user_profile
    )
    paginated_response = main.paginate(
        request, innovations, core_serializers.Innovation
    )
    return paginated_response


@api_view(["GET"])
def user_drafts(request):
    innovations = core_models.Innovation.objects.filter(
        author=request.user.user_profile, status="D"
    )
    paginated_response = main.paginate(
        request, innovations, core_serializers.Innovation
    )
    return paginated_response


@api_view(["POST"])
def publish_draft(request, pk):
    try:
        innovation = core_models.Innovation.objects.get(pk=pk)
    except core_models.Innovation.DoesNotExist:
        return Response(
            {"detail": "Innovation does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    innovation.status = "P"
    innovation.save()
    return Response(
        {"detail": "Published innovation successfully"}, status=status.HTTP_200_OK
    )

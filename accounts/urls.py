from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("djoser.urls")),
    path(
        "jwt/create/",
        view=views.CustomTokenObtainPairView.as_view(),
        name="token-obtain_pair",
    ),
    path(
        "jwt/refresh/",
        view=views.CustomTokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
        "jwt/verify/", view=views.CustomTokenVerifyView.as_view(), name="token-verify"
    ),
    path("logout/", view=views.LogoutView.as_view(), name="auth-logout"),
    path("profiles/", views.user_profile_list, name="userprofile-list"),
    path("profiles/<int:pk>/", views.user_profile_detail, name="userprofile-detail"),
]

from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("djoser.urls")),
    path(
        "jwt/create/",
        view=views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "jwt/refresh/",
        view=views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "jwt/verify/", view=views.CustomTokenVerifyView.as_view(), name="token_verify"
    ),
    path("logout/", view=views.LogoutView.as_view(), name="auth_logout"),
]

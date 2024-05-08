from django.urls import path
from . import views


urlpatterns = [
    path("innovations/", views.innovation_list, name="innovation-list"),
    path("innovations/<int:pk>/", views.innovation_detail, name="innovation-detail"),
    path(
        "innovations/<int:pk>/comments/",
        views.innovation_comment_list,
        name="innovationcomment-list",
    ),
    path(
        "comments/<int:pk>/",
        views.innovation_comment_detail,
        name="innovationcomment-detail",
    ),
]

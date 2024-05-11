from django.urls import path
from . import views


urlpatterns = [
    path("innovations/", views.innovation_list, name="innovation-list"),
    path("innovations/bookmarks/", views.bookmarks, name="bookmarks-list"),
    path("innovations/<int:pk>/", views.innovation_detail, name="innovation-detail"),
    path(
        "innovations/<int:pk>/bookmark/",
        views.bookmark_innovation,
        name="bookmark_innovation",
    ),
    path(
        "innovations/<int:pk>/unbookmark/",
        views.unbookmark_innovation,
        name="unbookmark_innovation",
    ),
    path("innovations/<int:pk>/like/", views.like_innovation, name="like_innovation"),
    path(
        "innovations/<int:pk>/unlike/",
        views.unlike_innovation,
        name="unlike_innovation",
    ),
    path(
        "innovations/<int:pk>/comments/",
        views.innovation_comment_list,
        name="innovation_comment-detail",
    ),
    path(
        "innovations/<int:pk>/comments/<int:cpk>/",
        views.innovation_comment_detail,
        name="innovation_comment-detail",
    ),
]

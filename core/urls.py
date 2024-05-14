from django.urls import path
from . import views


urlpatterns = [
    path("search/<str:query>/", views.search, name="search"),
    path("innovations/", views.innovation_list, name="innovation-list"),
    path("innovations/bookmarks/", views.user_bookmarks, name="bookmarks-list"),
    path(
        "innovations/likes/",
        views.user_innovation_like_list,
        name="user_innovation_like-list",
    ),
    path("innovations/<int:pk>/", views.innovation_detail, name="innovation-detail"),
    path("innovations/<int:pk>/export/", views.innovation_zip, name="innovation_zip"),
    path(
        "innovations/<int:pk>/bookmarks/",
        views.bookmark_innovation,
        name="bookmark_innovation",
    ),
    path(
        "innovations/<int:pk>/unbookmark/",
        views.unbookmark_innovation,
        name="unbookmark_innovation",
    ),
    path(
        "innovations/<int:pk>/likes/",
        views.innovation_like_list,
        name="innovation_like-list",
    ),
    path(
        "innovations/<int:pk>/unlike/",
        views.unlike_innovation,
        name="innovation_like-detail",
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

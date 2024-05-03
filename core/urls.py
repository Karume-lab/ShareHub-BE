from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("innovations/", views.innovation_list, name="innovation-list"),
    path(
        "innovations/<slug:slug>/", views.innovation_detail, name="innovation-detail"
    ),
]

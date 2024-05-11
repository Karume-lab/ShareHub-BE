from django.contrib import admin
from . import models


class InnovationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_at", "updated_at", "status")


class InnovationCommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "text",
        "created_at",
        "updated_at",
    )


class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "innovation",
    )


class BookmarkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "innovation",
    )


admin.site.register(models.Innovation, InnovationAdmin)
admin.site.register(models.InnovationComment, InnovationCommentAdmin)
admin.site.register(models.Like, LikeAdmin)
admin.site.register(models.Bookmark, BookmarkAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class CustomUserAdmin(UserAdmin):
    model = models.CustomUser
    list_display = (
        "id",
        "email",
        "is_staff",
        "is_active",
        "is_site_mod",
        "is_forum_mod",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_site_mod",
                    "is_forum_mod",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_site_mod",
                    "is_forum_mod",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "phone_number",
    )


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)

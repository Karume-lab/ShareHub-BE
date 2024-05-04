from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "is_active", "is_staff", "is_mod")
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_mod",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "username",
        "first_name",
        "last_name",
        "phone_number",
    )


admin.site.register(models.CustomUserModel, CustomUserAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)

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


admin.site.register(models.CustomUserModel, CustomUserAdmin)

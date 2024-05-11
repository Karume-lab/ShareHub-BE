from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from phonenumber_field.modelfields import PhoneNumberField
from . import managers
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_site_mod = models.BooleanField(default=False)
    is_forum_mod = models.BooleanField(default=False)

    objects = managers.UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    groups = models.ManyToManyField(
        "auth.Group", verbose_name="groups", blank=True, related_name="user_accounts"
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        related_name="user_accounts",
    )

    def __str__(self):
        return self.email

    def __repr__(self) -> str:
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        verbose_name=_("User"),
        related_name="user_profile",
        on_delete=models.CASCADE,
    )
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(_("Email"), max_length=254)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)
    phone_number = PhoneNumberField(blank=True)
    bio = models.TextField(_("Bio"), blank=True)
    profile_picture = models.ImageField(
        _("Profile Picture"),
        upload_to=f"media/profile_pictures",
        blank=True,
        null=True,
        height_field=None,
        width_field=None,
        max_length=None,
    )

    def save(self, *args, **kwargs):
        if self.user:
            self.profile_picture.upload_to = f"profile_images/{self.user.email}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email

    def __repr__(self) -> str:
        return self.user.email

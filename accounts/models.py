from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.contrib.auth.models import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_mod = models.BooleanField(default=False)

    objects = UserAccountManager()

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
        CustomUserModel, verbose_name=_("User"), on_delete=models.CASCADE
    )
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True)
    bio = models.TextField(_("Bio"))
    profile_picture = models.ImageField(
        _("Profile Picture"),
        upload_to=None,
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

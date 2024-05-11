from django.db import models
from django.utils.translation import gettext_lazy as _


class Innovation(models.Model):
    STATUS_CHOICES = (
        ("DE", "Deleted"),
        ("P", "Published"),
        ("D", "Draft"),
    )
    CATEGORY_CHOICES = (
        ("H", "HIV"),
        ("T", "Tuberculosis"),
        ("A", "Airborne"),
        ("W", "Waterborne"),
        ("O", "Other"),
    )
    author = models.ForeignKey(
        "accounts.UserProfile",
        on_delete=models.CASCADE,
        related_name="innovations",
    )
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    dashboard_link = models.URLField(
        _("Dashboard Link"), max_length=200, blank=True, null=True
    )
    dashboard_image = models.ImageField(
        _("Dashboard preview"),
        upload_to="media/dashboards",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True,
    )
    dashboard_definition = models.FileField(
        _("Dashboard and Dataset files"),
        upload_to="media/dashboard_definitions",
        max_length=100,
        blank=True,
        null=True,
    )
    banner_image = models.ImageField(
        _("Dashboard banner image"),
        upload_to="media/dashboards_banners",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)
    status = models.CharField(
        _("Status"), max_length=2, default="P", choices=STATUS_CHOICES
    )
    category = models.CharField(
        _("Category"), max_length=1, default="H", choices=CATEGORY_CHOICES
    )

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return self.title

    def get_is_liked(self, author):
        return Like.objects.filter(author=author, innovation=self).exists()


class Like(models.Model):
    author = models.ForeignKey(
        "accounts.UserProfile", on_delete=models.CASCADE, related_name="likes"
    )
    innovation = models.ForeignKey(
        Innovation, on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)

    def __str__(self) -> str:
        return self.innovation.title

    def __repr__(self) -> str:
        return self.innovation.title


class Forum(models.Model):
    pass


class InnovationComment(models.Model):
    author = models.ForeignKey(
        "accounts.UserProfile",
        on_delete=models.CASCADE,
        related_name="innovation_comments",
    )
    innovation = models.ForeignKey(
        "Innovation", on_delete=models.CASCADE, related_name="innovation_comments"
    )
    text = models.TextField(_("Comment"))
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)
    is_edited = models.BooleanField(_("Is edited"), default=False)


class ForumComment(models.Model):
    author = models.ForeignKey(
        "accounts.UserProfile", on_delete=models.CASCADE, related_name="forum_comments"
    )
    text = models.TextField(_("Comment"))
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)
    is_edited = models.BooleanField(_("Is edited"), default=False)
    likes = models.IntegerField(_("Likes"), default=0)

    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)

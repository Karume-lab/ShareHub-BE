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
    dataset = models.FileField(
        _("Dataset user"), upload_to="media/dataset", max_length=100
    )
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)
    status = models.CharField(
        _("Status"), max_length=2, default="P", choices=STATUS_CHOICES
    )
    category = models.CharField(
        _("Category"), max_length=1, default="H", choices=CATEGORY_CHOICES
    )
    likes = models.IntegerField(_("Likes"))

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return self.title


class Forum(models.Model):
    pass


class BaseComment(models.Model):
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE)
    text = models.TextField(_("Comment"))
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)
    likes = models.IntegerField(_("Likes"))

    class Meta:
        abstract = True


class InnovationComment(BaseComment):
    innovation = models.ForeignKey(
        "Innovation", on_delete=models.CASCADE, related_name="innovation_comments"
    )


class ForumComment(BaseComment):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)

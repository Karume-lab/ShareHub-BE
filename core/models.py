from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from datetime import datetime


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
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
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
    categories = models.CharField(
        _("Categories"), max_length=1, default="H", choices=CATEGORY_CHOICES
    )


    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return self.title

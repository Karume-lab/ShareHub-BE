from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model


class Innovation(models.Model):
    STATUS_CHOICES = (
        ("D", "Deleted"),
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
    dataset = models.FileField(_("Dataset user"), upload_to="media/innovation_cover_images", max_length=100)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date updated"), auto_now=True)
    status = models.CharField(
        _("Status"), max_length=1, default="P", choices=STATUS_CHOICES
    )
    categories = models.CharField(
        _("Categories"), max_length=1, default="P", choices=CATEGORY_CHOICES
    )
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.title}-{self.created_at}")
        super(Innovation, self).save(*args, **kwargs)

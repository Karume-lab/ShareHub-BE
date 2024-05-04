from django.contrib import admin
from . import models


class InnovationAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at", "status")


admin.site.register(models.Innovation, InnovationAdmin)

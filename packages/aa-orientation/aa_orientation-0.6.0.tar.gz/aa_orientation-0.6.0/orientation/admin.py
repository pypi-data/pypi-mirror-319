"""Admin site."""

from django.contrib import admin

from . import models

# Register your models for the admin site here.


admin.site.register(models.NewMembers)
admin.site.register(models.OrientationAppConfig)

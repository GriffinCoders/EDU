from django.contrib import admin

from . import models

admin.site.register(models.Term)
admin.site.register(models.College)
admin.site.register(models.Field)

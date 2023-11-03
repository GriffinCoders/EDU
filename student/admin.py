from django.contrib import admin

from . import models


admin.site.register(models.StudentProfile)
admin.site.register(models.StudentRequests)

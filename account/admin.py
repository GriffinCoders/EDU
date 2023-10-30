from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models


class UserAdmin(BaseUserAdmin):
    pass


admin.site.register(models.Term)
admin.site.register(models.College)
admin.site.register(models.Field)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.ProfessorProfile)
admin.site.register(models.StudentProfile)
admin.site.register(models.ItManagerProfile)
admin.site.register(models.EducationalAssistanceProfile)

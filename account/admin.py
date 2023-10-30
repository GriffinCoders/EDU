from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        ("", {"fields": ("profile_pic", "meli_code", "gender", "birth_date", "role")}),
    )


admin.site.register(models.Term)
admin.site.register(models.College)
admin.site.register(models.Field)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.ProfessorProfile)
admin.site.register(models.StudentProfile)
admin.site.register(models.ItManagerProfile)
admin.site.register(models.EducationalAssistanceProfile)

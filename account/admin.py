from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from educational_assistance.models import EducationalAssistanceProfile
from it_manager.models import ItManagerProfile
from professor.models import ProfessorProfile
from student.models import StudentProfile
from . import models


class EducationalAssistanceProfileInline(admin.StackedInline):
    model = EducationalAssistanceProfile


class ItManagerProfileInline(admin.StackedInline):
    model = ItManagerProfile


class ProfessorProfileInline(admin.StackedInline):
    model = ProfessorProfile


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile


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

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []

        profile_inline_classes = {
            '0': StudentProfileInline,
            '1': ProfessorProfileInline,
            '2': ItManagerProfileInline,
            '3': EducationalAssistanceProfileInline,
        }

        profile_inline_class = profile_inline_classes.get(obj.role, None)
        if profile_inline_class:
            return [profile_inline_class(self.model, self.admin_site)]
        else:
            return []


admin.site.register(models.User, UserAdmin)

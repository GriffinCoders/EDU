from rest_framework.permissions import BasePermission

from account.models import UserRoleChoices
from .models import StudentProfile


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == UserRoleChoices.Student and
            StudentProfile.objects.filter(user=request.user).exists()
        )

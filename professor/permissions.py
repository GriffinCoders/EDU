from rest_framework.permissions import BasePermission

from account.models import UserRoleChoices
from professor.models import ProfessorProfile


class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == UserRoleChoices.Professor and
            ProfessorProfile.objects.filter(user=request.user).exists()
        )

from rest_framework.permissions import BasePermission

from account.models import UserRoleChoices
from it_manager.models import ItManagerProfile


class IsItManager(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == UserRoleChoices.ItManager and
            ItManagerProfile.objects.filter(user=request.user).exists()
        )

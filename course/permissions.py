from rest_framework.permissions import BasePermission

from account.models import UserRoleChoices
from educational_assistance.models import EducationalAssistanceProfile
from it_manager.models import ItManagerProfile

    

class IsEducationalAssistanceOrItManager(BasePermission):
    def has_permission(self, request, view):
        
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == UserRoleChoices.EducationalAssistance and
            EducationalAssistanceProfile.objects.filter(user=request.user).exists() or 
            request.user.role == UserRoleChoices.ItManager and
            ItManagerProfile.objects.filter(user=request.user).exists()
            )
        )

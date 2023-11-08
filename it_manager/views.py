from rest_framework import viewsets
from .serializers import AssistantSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from educational_assistance.models import EducationalAssistanceProfile
from account.models import User



class ItMangerAssistantApiView(generics.ListCreateAPIView):
    queryset = EducationalAssistanceProfile.objects.all()
    serializer_class = AssistantSerializer


class ItMangerAssistantDtailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EducationalAssistanceProfile.objects.all()
    serializer_class = AssistantSerializer

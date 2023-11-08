from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from educational_assistance.models import EducationalAssistanceProfile
from common.models import Term, College
from common.serializers import TermSerializer, CollegeSerializer
from .permissions import IsItManager
from .serializers import AssistantSerializer



class ItMangerAssistantApiView(generics.ListCreateAPIView):
    queryset = EducationalAssistanceProfile.objects.all()
    serializer_class = AssistantSerializer


class ItMangerAssistantDtailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EducationalAssistanceProfile.objects.all()
    serializer_class = AssistantSerializer


class TermViewSet(viewsets.ModelViewSet):
    serializer_class = TermSerializer
    permission_classes = [IsAuthenticated, IsItManager]
    queryset = Term.objects.all()


class CollegeViewSet(viewsets.ModelViewSet):
    serializer_class = CollegeSerializer
    permission_classes = [IsAuthenticated, IsItManager]
    queryset = College.objects.all()

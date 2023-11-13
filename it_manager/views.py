from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from common.models import Term, College
from common.serializers import TermSerializer, CollegeSerializer
from professor.models import ProfessorProfile
from educational_assistance.models import EducationalAssistanceProfile
from educational_assistance.serializers import EducationalAssistanceSerializer
from professor.serializers import ProfessorSerializer
from .permissions import IsItManager


class ItMangerAssistantApiView(generics.ListCreateAPIView):
    queryset = EducationalAssistanceProfile.objects.all()
    permission_classes = [IsAuthenticated, IsItManager]
    serializer_class = EducationalAssistanceSerializer


class ItMangerAssistantDtailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EducationalAssistanceProfile.objects.all()
    permission_classes = [IsAuthenticated, IsItManager]
    serializer_class = EducationalAssistanceSerializer


class TermViewSet(viewsets.ModelViewSet):
    serializer_class = TermSerializer
    permission_classes = [IsAuthenticated, IsItManager]
    queryset = Term.objects.all()


class CollegeViewSet(viewsets.ModelViewSet):
    serializer_class = CollegeSerializer
    permission_classes = [IsAuthenticated, IsItManager]
    queryset = College.objects.all()


class ListProfessorProfile(ListModelMixin, generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsItManager]
    serializer_class = ProfessorSerializer
    pagination_class = PageNumberPagination
    page_size = 10

    def get_queryset(self):
        """
        Retrieves the queryset of ProfessorProfile objects based on the provided query parameters.

        Parameters:
            self (object): The instance of the class.
        
        Returns:
            queryset (QuerySet): The queryset of ProfessorProfile objects that match the provided query parameters.
        """
        queryset = ProfessorProfile.objects.all()

        name = self.request.query_params.get('first_name')
        last_name = self.request.query_params.get('last_name')
        professor_id = self.request.query_params.get('professor_id')
        meli_code = self.request.query_params.get('meli_code')
        college_name = self.request.query_params.get('college_name')
        field_name = self.request.query_params.get('field_name')
        order = self.request.query_params.get('order')

        if name:
            queryset = queryset.filter(user__first_name__icontains=name)
        if last_name:
            queryset = queryset.filter(user__last_name__icontains=last_name)
        if professor_id:
            queryset = queryset.filter(professor_id=professor_id)
        if meli_code:
            queryset = queryset.filter(national_id=meli_code)
        if college_name:
            queryset = queryset.filter(college__name__icontains=college_name)
        if field_name:
            queryset = queryset.filter(field__name__icontains=field_name)
        if order:
            queryset = queryset.filter(academic_rank=order)

        return queryset
    
    def get(self, request, *args, **kwargs):
        """
        Get method for the API endpoint.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object.
        """
        return self.list(request, *args, **kwargs)
    

class CreateProfessorProfileView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsItManager]
    serializer_class = ProfessorSerializer
    queryset = ProfessorProfile.objects.all()


class RetrieveProfessorProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsItManager]
    serializer_class = ProfessorSerializer
    queryset = ProfessorProfile.objects.all()


class UpdateProfessorProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsItManager]
    serializer_class = ProfessorSerializer
    queryset = ProfessorProfile.objects.all()


class DeleteProfessorProfileView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsItManager]
    queryset = ProfessorProfile.objects.all()

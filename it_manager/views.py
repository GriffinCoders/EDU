from rest_framework.generics import GenericAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
import professor
from professor.models import ProfessorProfile

# from .serializers import ProfessorProfileSerializer

class ListProfessorProfile(ListModelMixin, GenericAPIView):
    # serializer_class = ProfessorProfileSerializer
    pagination_class = PageNumberPagination
    page_size = 10

    def get_queryset(self):
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
        return self.list(request, *args, **kwargs)
    

class CreateProfessorProfileView(CreateModelMixin, GenericAPIView):
    # serializer_class = ProfessorProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return self.create(request, *args, **kwargs)

class RetrieveProfessorProfileView(RetrieveAPIView):
    # serializer_class = ProfessorProfileSerializer
    queryset = ProfessorProfile.objects.all()

class UpdateProfessorProfileView(UpdateAPIView):
    # serializer_class = ProfessorProfileSerializer
    queryset = ProfessorProfile.objects.all()

class DeleteProfessorProfileView(DestroyAPIView):
    queryset = ProfessorProfile.objects.all()

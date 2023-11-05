from django.urls import path
from .views import ListProfessorProfile, RetrieveProfessorProfileView, CreateProfessorProfileView, UpdateProfessorProfileView, DeleteProfessorProfileView

urlpatterns = [
    path('professors/', ListProfessorProfile.as_view(), name="list_professors"),
    path('professor/<int:pk>/', RetrieveProfessorProfileView.as_view(), name="detail_professor"),
    path('professors/create/', CreateProfessorProfileView.as_view(), name="create_professor"),
    path('professor/update/<int:pk>/', UpdateProfessorProfileView.as_view(), name="update_professor"),
    path('professor/delete/<int:pk>/', DeleteProfessorProfileView.as_view(), name="delete_professor"),
]

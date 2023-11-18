from django.urls import path
from rest_framework import routers

from . import views

app_name = "it_manager"

router = routers.DefaultRouter()
router.register('term', views.TermViewSet, basename='terms')
router.register('college', views.CollegeViewSet, basename='colleges')

urlpatterns = router.urls + [
    path('assistants/', views.ItMangerAssistantApiView.as_view()),
    path('assistant/<int:pk>/', views.ItMangerAssistantDtailView.as_view()),

    path('professors/', views.ListProfessorProfile.as_view(), name="list_professors"),
    path('professor/<int:pk>/', views.RetrieveProfessorProfileView.as_view(), name="detail_professor"),
    path('professors/create/', views.CreateProfessorProfileView.as_view(), name="create_professor"),
    path('professor/update/<int:pk>/', views.UpdateProfessorProfileView.as_view(), name="update_professor"),
    path('professor/delete/<int:pk>/', views.DeleteProfessorProfileView.as_view(), name="delete_professor"),

    path('students/', views.ListStudentProfile.as_view(), name="list_students"),
    path('student/<int:pk>/', views.RetrieveStudentProfileView.as_view(), name="detail_student"),
    path('students/create/', views.CreateStudentProfileView.as_view(), name="create_student"),
    path('student/update/<int:pk>/', views.UpdateStudentProfileView.as_view(), name="update_student"),
    path('student/delete/<int:pk>/', views.DeleteStudentProfileView.as_view(), name="delete_student"),
]

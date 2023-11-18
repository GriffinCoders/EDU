from django.urls import path

from rest_framework import routers

from . import views

app_name = "professor"

router = routers.DefaultRouter()
router.register('professor', views.ProfessorViewSet, basename='professor')

urlpatterns = router.urls + [
    path('students-selection-forms/<int:pk>', views.AcceptOrRejectStudentForm.as_view()),
    path('students-selection-forms-detail/<int:pk>', views.RetrieveStudentSelectionForm.as_view()),
    path('students-selection-forms/', views.ListStudentsSelectionForms.as_view()),
]


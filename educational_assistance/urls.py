from rest_framework import routers

from . import views

app_name = "educational_assistance"

router = routers.DefaultRouter()
router.register('student', views.AssistanceStudentViewSet, basename='students')
router.register('professor', views.AssistanceProfessorViewSet, basename='professors')

urlpatterns = router.urls

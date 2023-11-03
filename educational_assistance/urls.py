from django.urls import path

from rest_framework import routers

from . import views

app_name = "password"

router = routers.DefaultRouter()
router.register('student', views.StudentViewSet, basename='student')
router.register('professor', views.ProfessorViewSet, basename='professor')

urlpatterns = router.urls

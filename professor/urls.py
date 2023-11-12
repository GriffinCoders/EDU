from django.urls import path

from rest_framework import routers

from . import views

app_name = "professor"

router = routers.DefaultRouter()
router.register('professor', views.ProfessorViewSet, basename='professor')

urlpatterns = router.urls

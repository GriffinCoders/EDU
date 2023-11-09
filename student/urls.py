from django.urls import path

from rest_framework import routers

from . import views

app_name = "student"

router = routers.DefaultRouter()
router.register('student', views.StudentViewSet, basename='students')
router.register('course-selection', views.StudentCourseSelectionViewSet, basename='course_selections')

urlpatterns = router.urls

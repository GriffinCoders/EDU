from rest_framework import routers

from . import views

app_name = "student"

router = routers.DefaultRouter()
router.register('student', views.StudentViewSet, basename='students')

urlpatterns = router.urls

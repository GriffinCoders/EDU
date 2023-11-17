from rest_framework_nested import routers

from . import views

app_name = "student"

router = routers.DefaultRouter()
router.register('students', views.StudentViewSet, basename='students')
router.register('course-selections', views.StudentCourseSelectionRegistrationViewSet, basename='course_selections')

course_selection_router = routers.NestedSimpleRouter(router, 'course-selections', lookup='course_selection')
course_selection_router.register('courses', views.StudentCourseSelectionViewSet, basename='courses')

urlpatterns = router.urls + course_selection_router.urls

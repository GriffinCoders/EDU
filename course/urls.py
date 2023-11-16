from django.urls import path
from .views import LessonListView, LessonDetailView, CourseListView, CourseDetailView

urlpatterns = [
    path('subjects/', LessonListView.as_view(), name='lesson-create'),
    path('subjects/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),

    path('courses/', CourseListView.as_view(), name='course-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
]

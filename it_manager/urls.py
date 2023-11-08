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
]

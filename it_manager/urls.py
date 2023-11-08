from django.urls import path

from . import views

urlpatterns = [
    path('assistants/', views.ItMangerAssistantApiView.as_view()),
    path('assistant/<int:pk>/', views.ItMangerAssistantDtailView.as_view()),
]
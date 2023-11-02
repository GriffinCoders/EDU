from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.TokenLoginView.as_view(), name='login'),
    path('logout/', views.TokenLogoutView.as_view(), name='logout'),
]

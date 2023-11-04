from rest_framework import routers

from . import views

app_name = "it_manager"

router = routers.DefaultRouter()
router.register('term', views.TermViewSet, basename='terms')

urlpatterns = router.urls

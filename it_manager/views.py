from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from common.models import Term
from common.serializers import TermSerializer
from it_manager.permissions import IsItManager


class TermViewSet(viewsets.ModelViewSet):
    serializer_class = TermSerializer
    permission_classes = [IsAuthenticated, IsItManager]
    queryset = Term.objects.all()

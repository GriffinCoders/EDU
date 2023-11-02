from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from . import serializers


class TokenLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class TokenLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            Token.objects.get(user=request.user).delete()
        except Token.DoesNotExist:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

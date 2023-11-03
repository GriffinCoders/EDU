import random

from django.core.cache import cache

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from . import serializers
from .models import User


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


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=ser.validated_data.get('email'))
        except User.DoesNotExist:
            return Response({"msg": "User not found!"}, status=status.HTTP_400_BAD_REQUEST)
        user_otp = ser.validated_data.get("otp", None)
        new_password = ser.validated_data.get("new_password", None)
        cache_prefix = ser.validated_data.get("email") + "_otp"
        if not user_otp:
            cached_otp = cache.get(cache_prefix, None)
            if not cached_otp:
                random.seed()
                otp = str(random.randint(111111, 999999))
                # TODO: send the otp
                print("otp: " + otp)
                cache.set(cache_prefix, otp, timeout=3600)
                return Response({"msg": "Otp sent"}, status.HTTP_200_OK)
            else:
                return Response({"msg": "Otp already sent"}, status=status.HTTP_400_BAD_REQUEST)
        if not user_otp or not new_password:
            return Response({"msg": "Must include otp and new password"}, status=status.HTTP_400_BAD_REQUEST)
        cached_otp = cache.get(cache_prefix, None)
        if not user_otp == cached_otp:
            return Response({"msg": "Invalid otp"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"msg": "New password saved"}, status=status.HTTP_200_OK)

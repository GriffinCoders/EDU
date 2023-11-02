from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
        write_only=True
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError({"msg": msg}, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError({"msg": msg}, code='authorization')

        attrs['user'] = user
        return attrs

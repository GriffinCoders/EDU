from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile_pic', 'meli_code', 'gender', 'birth_date', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
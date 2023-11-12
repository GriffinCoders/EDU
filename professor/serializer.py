from rest_framework import serializers

from account.models import User
from account.serializer import UserSerializer
from .models import ProfessorProfile
from common.models import College, Field

class ProfessorProfileSerializer(serializers.ModelSerializer):
    college = serializers.PrimaryKeyRelatedField(queryset=College.objects.all())  
    field = serializers.PrimaryKeyRelatedField(queryset=Field.objects.all())
    user = UserSerializer()

    class Meta:
        model = ProfessorProfile
        fields = ['user', 'college', 'field', 'orientation', 'order', 'id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')  
        user, created = User.objects.get_or_create(**user_data)
        validated_data['user'] = user  
        professor_profile = ProfessorProfile.objects.create(**validated_data)
        return professor_profile

    
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
    

    def to_representation(self, instance):
        """
        Generate the representation of an instance.

        Args:
            instance: The instance to represent.

        Returns:
            The representation of the instance.

        """
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation

    def create(self, validated_data):
        """
        Create a new professor profile using the provided validated data.

        Args:
            validated_data (dict): A dictionary containing the validated data for creating the professor profile.

        Returns:
            ProfessorProfile: The newly created professor profile object.
        """
        user_data = validated_data.get('user', {})  
        user, created = User.objects.get_or_create(**user_data)
        validated_data['user'] = user
        professor_profile = ProfessorProfile.objects.create(**validated_data)
        return professor_profile
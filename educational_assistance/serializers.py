from rest_framework import serializers

from account.serializers import UserSerializer
from educational_assistance.models import EducationalAssistanceProfile
from account.models import User, UserRoleChoices
from utils.user_profile import update_user_profile


class EducationalAssistanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = EducationalAssistanceProfile
        fields = [
            "id",
            "user",
            "college",
            "field",
        ]

    def create(self, validated_data):
        # get a user
        user_data = validated_data.pop('user')
        # create an instance of the user
        user = User.objects.create(**user_data, role=UserRoleChoices.EducationalAssistance)
        validated_data['user'] = user

        return EducationalAssistanceProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return update_user_profile(instance, validated_data)

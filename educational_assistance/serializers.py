from rest_framework import serializers

from account.serializers import UserSerializer
from educational_assistance.models import EducationalAssistanceProfile
from account.models import User, UserRoleChoices


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
        user_data = validated_data.pop('user')

        # Update Profile Picture of user if exists
        profile_pic = user_data.pop('profile_pic')
        if profile_pic:
            setattr(instance.user, 'profile_pic', profile_pic)

        # Update the user
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        # Update the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.user.save()
        instance.save()

        return instance

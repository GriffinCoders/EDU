from rest_framework import serializers

from account.serializers import UserSerializer
from .models import StudentProfile


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "user",
            "entry_year",
            "entry_term",
            "college",
            "field",
            "military_status",
            "valid_years",
            "supervisor",
            "grade",
            "created_at",
            "updated_at",
        ]

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

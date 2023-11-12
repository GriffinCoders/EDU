from rest_framework import serializers

from account.models import User, UserRoleChoices
from account.serializers import UserSerializer
from utils.user_profile import update_user_profile
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

    def create(self, validated_data):
        # get a user
        user_data = validated_data.pop('user')
        # create an instance of the user
        user = User.objects.create(**user_data, role=UserRoleChoices.Student)
        validated_data['user'] = user

        return StudentProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return update_user_profile(instance, validated_data)

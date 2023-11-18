from rest_framework import serializers

from account.models import User, UserRoleChoices
from account.serializers import UserSerializer
from utils.user_profile import update_user_profile
from .models import ProfessorProfile


class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProfessorProfile
        fields = [
            "id",
            "user",
            "college",
            "field",
            "orientation",
            "order",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        # get a user
        user_data = validated_data.pop('user')
        # create an instance of the user
        user = User.objects.create(**user_data, role=UserRoleChoices.Professor)
        validated_data['user'] = user

        return ProfessorProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return update_user_profile(instance, validated_data)

class AcceptOrRejectStudentFormSerializer(serializers.Serializer):
    is_accepted = serializers.BooleanField()



    


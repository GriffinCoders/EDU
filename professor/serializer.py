from venv import create
from rest_framework import serializers

from account.models import User
from account.serializer import UserSerializer
from .models import ProfessorProfile
# from common.serializer import CollegeSerializer, FieldSerializer
from common.models import College, Field
# from account.serializer import UserSerializer

# class ProfessorProfileSerializer(serializers.ModelSerializer):
#     # college = CollegeSerializer(read_only=True)
#     # field = FieldSerializer(read_only=True)

#     college = CollegeSerializer()
#     field = FieldSerializer()
#     user = UserSerializer()
#     class Meta:
#         model = ProfessorProfile
#         fields = ['user', 'college', 'field', 'orientation', 'order', 'id', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'created_at', 'updated_at']



#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         college_data = validated_data.pop('college')
#         field_data = validated_data.pop('field')

#         user, created = User.objects.get_or_create(**user_data)

#         college, created = College.objects.get_or_create(**college_data)

#         field, created = Field.objects.get_or_create(**field_data)

#         validated_data['user'] = user
#         validated_data['college'] = college
#         validated_data['field'] = field

#         professor_profile = ProfessorProfile.objects.create(**validated_data)

#         return professor_profile
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

    
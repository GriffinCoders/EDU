from rest_framework import serializers
from .models import ProfessorProfile
from common.serializer import CollegeSerializer, FieldSerializer

class ProfessorProfileSerializer(serializers.ModelSerializer):
    college = CollegeSerializer()
    field = FieldSerializer()

    class Meta:
        model = ProfessorProfile
        fields = ['user', 'college', 'field', 'orientation', 'order', 'id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
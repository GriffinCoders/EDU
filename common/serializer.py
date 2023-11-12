from rest_framework import serializers
from .models import College, Field

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['name', 'id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    

class FieldSerializer(serializers.ModelSerializer):
    college = serializers.PrimaryKeyRelatedField(queryset=College.objects.all())

    class Meta:
        model = Field
        fields = ['id', 'name', 'educational_group', 'college', 'units', 'grade', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
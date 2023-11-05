from rest_framework import serializers
from .models import College, Field

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['name', 'id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
# class FieldSerializer(serializers.ModelSerializer):
#     college = CollegeSerializer()

#     class Meta:
#         model = Field
#         fields = ['id', 'name', 'educational_group', 'college', 'units', 'grade', 'created_at', 'updated_at']
#         read_only_fields = ['id', 'created_at', 'updated_at']
    
#     def create(self, validated_data):
#         college_data = validated_data.pop('college')
        
#         college, created = College.objects.get_or_create(**college_data)

#         validated_data['college'] = college  
#         validated_data['college_id'] = college.id
#         field = Field.objects.create(**validated_data)

#         return field
class FieldSerializer(serializers.ModelSerializer):
    college = serializers.PrimaryKeyRelatedField(queryset=College.objects.all())

    class Meta:
        model = Field
        fields = ['id', 'name', 'educational_group', 'college', 'units', 'grade', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
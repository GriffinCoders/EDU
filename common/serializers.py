from rest_framework import serializers

from .models import Term, College, Field


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = [
            "id",
            "name",
            "selection_start",
            "selection_finish",
            "class_start",
            "class_finish",
            "substitution_start",
            "substitution_finish",
            "emergency_removal_finish",
            "exams_start",
            "term_finish",
            'created_at',
            'updated_at',
        ]


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = [
            "id",
            "name",
            'created_at',
            'updated_at',
        ]


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = [
            'id',
            'name',
            'educational_group',
            'college',
            'units',
            'grade',
            'created_at',
            'updated_at',
        ]

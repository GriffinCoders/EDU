from rest_framework import serializers

from common.models import Term


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
        ]

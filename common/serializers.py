from rest_framework import serializers

from common.models import Term, College


class CustomChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


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
            "include_valid_years",
        ]


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = [
            "id",
            "name",
        ]

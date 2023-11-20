from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import Term, College, Field


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
            'created_at',
            'updated_at',
        ]
        labels = {
            "name": _("Name"),
            "selection_start": _("Selection Start"),
            "selection_finish": _("Selection Finish"),
            "class_start": _("Class Start"),
            "class_finish": _("Class Finish"),
            "substitution_start": _("Substitution Start"),
            "substitution_finish": _("Substitution Finish"),
            "emergency_removal_finish": _("Emergency Removal Finish"),
            "exams_start": _("Exams Start"),
            "term_finish": _("Term Finish"),
            "include_valid_years": _("Include Valid Years"),
            'created_at': _("Created at"),
            'updated_at': _("Updated at"),
        }


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = [
            "id",
            "name",
            'created_at',
            'updated_at',
        ]
        labels = {
            "name": _("Name"),
            'created_at': _("Created at"),
            'updated_at': _("Updated at"),
        }


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
        labels = {
            'name': _("Name"),
            'educational_group': _("Educational Group"),
            'college': _("College"),
            'units': _("Units"),
            'grade': _("Grade"),
            'created_at': _("Created at"),
            'updated_at': _("Updated at"),
        }

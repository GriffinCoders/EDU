from common.models import College, Field
import pytest

@pytest.fixture
def college_data(db):
    """
    Fixture to create and return college data.
    """
    college = College.objects.create(
        name="Test College", 
        )

    return {
        "college": college,
        "college_name": college.name,
        "college_id": college.id,
        "college_created_at" : college.created_at,
        "college_updated_at" : college.updated_at,
    }

@pytest.fixture
def field_data(db, college_data):
    """
    Fixture to create and return field data.
    """
    field = Field.objects.create(
        name="Test Field",
        educational_group="Test Educational Group",
        college=college_data["college"],
        units=10,
        grade="A",
    )
    
    return {
        "field": field,
        "field_name": field.name,
        "field_id": field.id,
        "field_created_at" : field.created_at,
        "field_updated_at" : field.updated_at,
        "field_college_name": field.college.name,
        "field_college_id": field.college.id,
        "field_educational_group": field.educational_group,
        "field_units": field.units,
        "field_grade": field.grade,
    }

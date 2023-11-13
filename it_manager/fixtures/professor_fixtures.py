import pytest
@pytest.fixture
def professor_data(user_data, college_data, field_data):
    """
    Fixture to create and return professor data.
    """
    return {
        "user": user_data["user"].id,
        "college": college_data["college"].id,
        "field": field_data["field"].id,
        "orientation": "Test Professor Orientation",
        "order": "Test Professor Order",
    }

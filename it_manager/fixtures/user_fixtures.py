from account.models import User
import pytest

@pytest.fixture
def user_data(db):
    """
    Fixture to create and return user data.
    """
    user = User.objects.create(
        first_name="test_first_name",
        last_name="test_last_name",
        meli_code="0025065487",
        gender="M",
        birth_date="2000-01-01",
        email="alex@gmail.com",
    )

    return {
        "user": user,
        "password": user.password,
        "meli_code": user.meli_code,
        "gender": user.gender,
        "birth_date": user.birth_date,
        "email": user.email,
        "role": user.role,
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

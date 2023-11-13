from account.models import User, UserRoleChoices
from professor.models import ProfessorProfile
from it_manager.models import ItManagerProfile
from common.models import College, Field
import pytest
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
        role=UserRoleChoices.Professor,
    )

    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "profile_pic": None,
        "meli_code": user.meli_code,
        "gender": user.gender,
        "birth_date": user.birth_date,
        "email": user.email,
    }

@pytest.fixture
def it_manager_user():
    """
    Fixture to create an "it_manager" user with all permissions.
    """
    user = User.objects.create(
        first_name="test_it_manager_name",
        last_name="test_it_manager_last_name",
        meli_code="0029065987",
        gender="M",
        birth_date="1993-01-01",
        email="itmanager@gmail.com",
        is_staff=True,
        is_superuser=True,
        role=UserRoleChoices.ItManager,
    )
    ItManagerProfile.objects.create(user=user)
    return user

@pytest.fixture
def oridionary_user():
    user = User.objects.create(
        first_name="oridionary_user_name",
        last_name="oridionary_user_last_name",
        meli_code="0069852369",
        gender="F",
        birth_date="1993-01-01",
        email="ordionaryuser@gmail.com",
        role=UserRoleChoices.Student,
    )
    return user


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


@pytest.fixture
def professor_data(user_data, college_data, field_data):
    """
    Fixture to create and return professor data.
    """
    return {
        "user": user_data,
        "college": college_data["college"].id,
        "field": field_data["field"].id,
        "orientation": "Test Professor Orientation",
        "order": "Test Professor Order",
    }

@pytest.fixture
def professor_instance_one(college_data, field_data):
    user = User.objects.create(
        first_name="test_list_first_name_user_one",
        last_name="test_list_last_name_user_one",
        meli_code="0055065487",
        gender="M",
        birth_date="2000-01-01",
        email="alextest@gmail.com",
        role=UserRoleChoices.Professor,
    )

    professor = ProfessorProfile.objects.create(
        user=user,
        college=college_data["college"],
        field=field_data["field"],
        orientation= "Test Professor Orientation",
        order= "Test Professor Order",
    )
    
    return professor

@pytest.fixture
def professor_instance_two(college_data, field_data):
    user = User.objects.create(
        first_name="test_list_first_name_user_two",
        last_name="test_list_last_name_user_two",
        meli_code="0055065407",
        gender="M",
        birth_date="2000-01-01",
        email="alextesdt@gmail.com",
        role=UserRoleChoices.Professor,
    )

    professor = ProfessorProfile.objects.create(
        user=user,
        college=college_data["college"],
        field=field_data["field"],
        orientation= "Test Professor Orientation",
        order= "Test Professor Order",
    )

    return professor

@pytest.fixture
def professor_instance_three(college_data, field_data):
    user = User.objects.create(
        first_name="test_list_first_name_user_three",
        last_name="test_list_last_name_user_three",
        meli_code="0055065400",
        gender="M",
        birth_date="2000-01-01",
        email="alextesdddt@gmail.com",
        role=UserRoleChoices.Professor,
    )

    professor = ProfessorProfile.objects.create(
        user=user,
        college=college_data["college"],
        field=field_data["field"],
        orientation= "Test Professor Orientation",
        order= "Test Professor Order",
    )

    return professor
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from account.factories import UserFactory
from common.factories import FieldFactory, CollegeFactory
from professor.factories import ProfessorProfileFactory
from professor.serializer import ProfessorProfileSerializer
import pytest

@pytest.mark.django_db
class TestProfessorCreation:
    @pytest.mark.skip
    def test_if_user_is_anonymous(self):
        """
        This is a test function to check if the user is anonymous.
        It creates an instance of the APIClient class and a professor profile using the ProfessorProfileFactory class.
        Then it creates an instance of the ProfessorProfileSerializer class using the professor profile.
        Next, it sends a POST request to the 'create_professor' endpoint with the serialized data.
        Finally, it asserts that the response status code is HTTP 401 Unauthorized.
        """
        client = APIClient()
        professor_profile = ProfessorProfileFactory()
        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.post(reverse('create_professor'), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.skip
    def test_if_user_is_not_authorized(self):
        """
        Test if the user is not authorized to create a professor.

        Parameters:
            self (object): The current object.
        
        Returns:
            None
        
        Raises:
            AssertionError: If the response status code is not equal to HTTP_403_FORBIDDEN.
        """
        client = APIClient()
        professor_profile = ProfessorProfileFactory()
        client.force_authenticate(user=professor_profile.user)
        serializer_instance = professor_profile.ProfessorProfileSerializer(professor_profile)

        response = client.post(reverse('create_professor'), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_correct_user_with_invalid_date(self):
        """
        Test the behavior of the function when the user is correct but the date is invalid.
        """
        client = APIClient()
        professor_profile = ProfessorProfileFactory()
        serializer_instance = ProfessorProfileSerializer(professor_profile)
        serializer_instance.data['user']['role'] = '12'

        response = client.post(reverse('create_professor'), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


    def test_correct_user_valid_data(self):
        """
        Test the function test_correct_user_valid_data.

        This function tests the functionality of the test_correct_user_valid_data method in the current class.

        Parameters:
            self (TestClass): The current instance of the TestClass.

        Returns:
            None
        """
        client = APIClient()
        user = UserFactory()
        college = CollegeFactory()
        field = FieldFactory(college=college)
        professor_profile = ProfessorProfileFactory(user=user, college=college, field=field)
        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.post(reverse('create_professor'), data=serializer_instance.data, format='json')


from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
import pytest

from it_manager.tests.conftest import ordinary_user


@pytest.fixture
def api_client():
    """
    Fixture to create and return a DRF API client.
    """
    return APIClient()


@pytest.fixture
def make_authenticated_request(api_client):
    """
    Fixture to make HTTP requests to a specified DRF url.
    """
    def make_http_request(method, url_name, args = None, data=None, format='json', user=None):
        if user:
            api_client.force_authenticate(user=user)

        url = reverse(url_name, args=args)
        request_func = getattr(api_client, method.lower())

        if method in ('GET', 'DELETE'):
            response = request_func(url)
        else:
            response = request_func(url, data=data, format=format)

        return response

    return make_http_request

@pytest.fixture
def make_not_authenticated_request(api_client):
    """
    Fixture to make HTTP requests to a specified DRF url.
    """
    def make_http_request(method, url_name, args = None, data=None, format='json'):
        
        url = reverse(url_name, args=args)
        request_func = getattr(api_client, method.lower())

        if method in ('GET', 'DELETE'):
            response = request_func(url)
        else:
            response = request_func(url, data=data, format=format)

        return response

    return make_http_request


@pytest.mark.django_db
class TestProfessorCreation:
    def test_if_user_is_anonymous(self, make_not_authenticated_request, professor_data):
        """
        Checks if the user is anonymous by making a not authenticated request to create a professor with the given professor data.

        Parameters:
            make_not_authenticated_request (function): A function that makes a not authenticated request.
            professor_data (dict): The data of the professor to be created.

        Returns:
            None

        Raises:
            AssertionError: If the response status code is not HTTP_401_UNAUTHORIZED.
        """


        professor = professor_data

        response = make_not_authenticated_request('POST', 'it_manager:create_professor', data=professor, format='json')
        print(response.content)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_authorized(self, make_authenticated_request, professor_data, ordinary_user):
        """
        Test if the user is not authorized to create a professor.

        Args:
            make_authenticated_request (function): A function to make an authenticated request.
            professor_data (dict): The professor data to be used for the request.
            oridionary_user (str): The user making the request.

        Returns:
            None

        Raises:
            AssertionError: If the response status code is not 403 Forbidden.
        """
       
        
        professor = professor_data

        response = make_authenticated_request('POST', 'it_manager:create_professor', data=professor, format='json', user=ordinary_user)
     
        assert response.status_code == status.HTTP_403_FORBIDDEN, "Expected 403 Forbidden status code"

    def test_correct_user_with_invalid_data(self, make_authenticated_request, professor_data, it_manager_user):
        """
        Test if the function correctly handles a user with invalid data.

        Args:
            make_authenticated_request (function): A function that makes an authenticated request.
            professor_data (dict): The data of the professor.
            it_manager_user (User): The user object of the IT manager.

        Returns:
            None
        """
        

        professor = professor_data
        professor['user']['gender'] = 'invalid'
        
        response = make_authenticated_request('POST', 'it_manager:create_professor', data=professor, format='json', user=it_manager_user)

        print(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_correct_user_with_valid_data(self, make_authenticated_request, professor_data, it_manager_user):
        """
        Test the functionality of creating a professor with valid data and a correct user.
        
        Args:
            make_authenticated_request (function): A function that makes an authenticated request.
            professor_data (dict): The data of the professor to be created.
            it_manager_user (User): The user with IT manager privileges.
        
        Returns:
            None
        """

        professor = professor_data

        response = make_authenticated_request('POST', 'it_manager:create_professor', data=professor, format='json', user=it_manager_user)

        assert response.status_code == status.HTTP_201_CREATED



class TestProfessorRetrieve:
    def test_if_user_is_anonymous(self, make_not_authenticated_request, professor_instance_one):
        """
        Tests whether the user is anonymous by making a not authenticated request to the detail_professor endpoint for a given professor instance. 

        Args:
            make_not_authenticated_request (function): A function that makes a not authenticated request.
            professor_instance_one (object): An instance of the professor class.

        Returns:
            None
        """
        
        
        professor = professor_instance_one

        response = make_not_authenticated_request('GET', 'it_manager:detail_professor', args=[professor.id], format='json')
        

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_authorized(self, make_authenticated_request, professor_instance_one, ordinary_user):
        """
        Check if the user is not authorized to perform a certain action.

        Args:
            make_authenticated_request (function): The function used to make authenticated requests.
            professor_instance_one (Professor): An instance of the Professor class.
            oridionary_user (User): An instance of the User class representing an ordinary user.

        Returns:
            None
        """

        professor = professor_instance_one

        response = make_authenticated_request('GET', 'it_manager:detail_professor', args=[professor.id], format='json', user=ordinary_user)

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_user_is_it_manager(self, make_authenticated_request, professor_instance_one, it_manager_user):
        """
        This function tests if a user is an IT manager.

        Args:
            make_authenticated_request (function): A function that makes an authenticated request.
            professor_instance_one (Professor): An instance of the Professor class.
            it_manager_user (User): An instance of the User class representing an IT manager.

        Returns:
            None
        """

        professor = professor_instance_one

        response = make_authenticated_request('GET', 'it_manager:detail_professor', args=[professor.id], format='json', user=it_manager_user)

        assert response.status_code == status.HTTP_200_OK


class TestProfessorList:
    def test_if_user_is_anonymous(self, make_not_authenticated_request, professor_instance_one, professor_instance_two, professor_instance_three):
        """
        Test if the user is anonymous.

        Parameters:
            make_not_authenticated_request (function): A function that makes a not authenticated request.
            professor_instance_one (object): An instance of a professor.
            professor_instance_two (object): An instance of a professor.
            professor_instance_three (object): An instance of a professor.

        Returns:
            None
        """

        professor1 = professor_instance_one
        professor2 = professor_instance_two
        professor3 = professor_instance_three

        response = make_not_authenticated_request('GET', 'it_manager:list_professors', format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

    def test_if_user_is_not_authorized(self, make_authenticated_request, professor_instance_one, professor_instance_two, professor_instance_three,
                                       ordinary_user):
        """
        Check if the user is not authorized to access a specific resource.

        Args:
            make_authenticated_request (function): A function that makes an authenticated request.
            professor_instance_one (Professor): An instance of the Professor class.
            professor_instance_two (Professor): An instance of the Professor class.
            professor_instance_three (Professor): An instance of the Professor class.
            oridionary_user (User): An instance of the User class representing an ordinary user.

        Returns:
            None
        """

        professor1 = professor_instance_one
        professor2 = professor_instance_two
        professor3 = professor_instance_three

        response = make_authenticated_request('GET', 'it_manager:list_professors', format='json', user=ordinary_user)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_it_manager(self, make_authenticated_request, professor_instance_one, professor_instance_two, professor_instance_three, it_manager_user):
        """
        Test if the user is an IT manager.

        This function creates a test client and makes a GET request to the 'detail_professor' endpoint.
        It then checks if the response status code is equal to 200, indicating a successful request.

        Parameters:
        - self: The current instance of the test case.

        Return:
        - None
        """
        professor1 = professor_instance_one
        professor2 = professor_instance_two
        professor3 = professor_instance_three

        response = make_authenticated_request('GET', 'it_manager:list_professors', format='json', user=it_manager_user)

        assert response.status_code == status.HTTP_200_OK, "Expected 200 OK status code"


class TestProfessorUpdate:
    def test_if_user_is_anonymous(self, make_not_authenticated_request, professor_data, professor_instance_one):
        """
        Check if a user is anonymous by making a not authenticated request to update a professor's data.

        Parameters:
            make_not_authenticated_request (function): A function that makes a not authenticated request.
            professor_data (dict): The updated data for the professor.
            professor_instance_one (Professor): An instance of the Professor class.

        Returns:
            None

        Raises:
            AssertionError: If the response status code is not 401 Unauthorized.
        """


        professor = professor_instance_one
        updated_professor_data_professor = professor_data

        response = make_not_authenticated_request('PUT', 'it_manager:update_professor', args=[professor.id], data=updated_professor_data_professor, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

    def test_if_user_is_not_authorized(self, make_authenticated_request, professor_data, professor_instance_one,
                                       ordinary_user):
        """
        Test if the user is not authorized to update a professor.
        
        Args:
            make_authenticated_request (function): A function used to make an authenticated request.
            professor_data (dict): The updated data for the professor.
            professor_instance_one (Professor): An instance of the Professor model.
            oridionary_user (User): The user making the request.
        
        Returns:
            None
        """

        professor = professor_instance_one
        updated_professor_data_professor = professor_data

        response = make_authenticated_request('PUT', 'it_manager:update_professor', args=[professor.id], data=updated_professor_data_professor, format='json', user=ordinary_user)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_it_manager(self, make_authenticated_request, professor_data, professor_instance_one, it_manager_user):
        """
        Test if the user is an IT manager.

        Args:
            make_authenticated_request (function): A function to make an authenticated request.
            professor_data (dict): Data of the professor.
            professor_instance_one (Professor): An instance of the Professor class.
            it_manager_user (User): An instance of the User class representing an IT manager.

        Returns:
            None
        """

        professor = professor_instance_one
        updated_professor_data_professor = professor_data

        response = make_authenticated_request('PUT', 'it_manager:update_professor', args=[professor.id], data=updated_professor_data_professor, format='json', user=it_manager_user)
        print(response.content)
        assert response.status_code == status.HTTP_205_RESET_CONTENT, "Expected 205 Reset Content status code"


class TestProfessorDelete:
    def test_if_user_is_anonymous(self, make_not_authenticated_request, professor_instance_one):
        """
        Check if the user is anonymous by making a not authenticated request.
        
        Args:
            make_not_authenticated_request: A function that makes a not authenticated request.
            professor_instance_one: An instance of the professor class.
        
        Returns:
            None
        """

        professor = professor_instance_one

        response = make_not_authenticated_request('DELETE', 'it_manager:delete_professor', args=[professor.id], data=professor, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

    def test_if_user_is_not_authorized(self, make_authenticated_request, professor_instance_one, ordinary_user):
        """
        Test if the user is anonymous.

        This function creates a test client and sets up the necessary objects for testing. It then calls the API endpoint for deleting a professor profile with the given professor profile ID. The function asserts that the response status code is 401 UNAUTHORIZED, indicating that the user is not authenticated.

        Parameters:
            self (obj): The current instance of the test case.

        Returns:
            None
        """

        professor = professor_instance_one

        response = make_authenticated_request('DELETE', 'it_manager:delete_professor', args=[professor.id], data=professor, format='json', user=ordinary_user)

        assert response.status_code == status.HTTP_403_FORBIDDEN


    def test_if_user_is_it_manager(self, make_authenticated_request, professor_instance_one, it_manager_user):
        """
        Test if the user is an IT manager.

        This function creates a test scenario by instantiating various objects such as `client`, `user`, `college`, `field`, and `professor_profile`. It then creates an instance of the `ProfessorProfileSerializer` using the `professor_profile` object.

        The function sends a DELETE request to the 'delete_professor' endpoint with the `professor_profile` ID as a path parameter and the serialized data as the request payload. The expected response status code is `204 No Content`.

        Raises:
            AssertionError: If the response status code is not `204 No Content`.

        Parameters:
            self (TestUserManager): The current instance of the test case.

        Returns:
            None
        """
        professor = professor_instance_one

        response = make_authenticated_request('DELETE', 'it_manager:delete_professor', args=[professor.id], data=professor, format='json', user=it_manager_user)

        assert response.status_code == status.HTTP_204_NO_CONTENT, "Expected 204 No Content status code"






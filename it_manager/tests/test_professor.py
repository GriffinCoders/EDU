from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
import pytest

from it_manager.tests.conftest import oridionary_user


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
    def make_http_request(method, url_name, data=None, format='json', user=None):
        if user:
            api_client.force_authenticate(user=user)

        url = reverse(url_name)
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
    def make_http_request(method, url_name, data=None, format='json'):
        
        url = reverse(url_name)
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
        Test if the user is anonymous.

        This function creates a test client, a college, a field, and a professor profile using the 'baker' library.
        It then creates an instance of the 'ProfessorProfileSerializer' class with the created professor profile.
        Next, it sends a post request to the 'create_professor' endpoint with the serialized data.
        Finally, it asserts that the response status code is equal to 401 (Unauthorized).

        Parameters:
            self (TestClass): The instance of the test class.

        Returns:
            None
        """

        professor = professor_data

        response = make_not_authenticated_request('POST', 'it_manager:create_professor', data=professor, format='json')
        print(response.content)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_authorized(self, make_authenticated_request, professor_data, oridionary_user):
        """
        Test if the user is not authorized to create a professor profile.

        This function performs the following steps:
        1. Creates an instance of the `APIClient` class.
        2. Creates a `College` object using the `baker.make` function.
        3. Creates a `Field` object using the `baker.make` function, with the `college` parameter set to the previously created `College` object.
        4. Creates a `ProfessorProfile` object using the `baker.make` function, with the `college` parameter set to the previously created `College` object and the `field` parameter set to the previously created `Field` object.
        5. Authenticates the client with the user associated with the `ProfessorProfile` object.
        6. Creates an instance of the `ProfessorProfileSerializer` class, with the `professor_profile` parameter set to the previously created `ProfessorProfile` object.
        7. Sends a `POST` request to the `create_professor` endpoint, with the request body set to the serialized data of the `ProfessorProfile` object.
        8. Asserts that the response status code is `403 Forbidden`.

        This function is used to test the behavior of the API when a user is not authorized to create a professor profile.

        Parameters:
        - self: The current instance of the class.

        Returns:
        This function does not return any value.
        """
        
        professor = professor_data

        response = make_authenticated_request('POST', 'it_manager:create_professor', data=professor, format='json', user=oridionary_user)
     
        assert response.status_code == status.HTTP_403_FORBIDDEN, "Expected 403 Forbidden status code"

    def test_correct_user_with_invalid_data(self, make_authenticated_request, professor_data, it_manager_user):
        """
        Test case for checking if the function correctly handles the scenario where a user with invalid data is passed.

        This test case creates a test client and generates some test data using the `baker` library. It then creates a `ProfessorProfileSerializer` instance and modifies the `user` role to an invalid value.

        The test client sends a POST request to the `create_professor` endpoint with the modified serializer data. The expected response status code is `400 Bad Request`.

        Raises:
            AssertionError: If the response status code is not `400 Bad Request`.

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
        Test the scenario where the user is correct and the data is valid.
        
        Args:
            make_authenticated_request (function): A function to make an authenticated request.
            professor_data (dict): The data for the professor.
            it_manager_user (User): The user with IT manager privileges.
            
        Returns:
            None
        """

        professor = professor_data

        response = make_authenticated_request('POST', 'it_manager:create_professor', data=professor, format='json', user=it_manager_user)

        assert response.status_code == status.HTTP_201_CREATED



# class TestProfessorRetrieve:
#     def test_if_user_is_anonymous(self):
#         """
#         Test if the user is anonymous.

#         This function creates a test environment by creating instances of various model classes such as User, College, Field, and ProfessorProfile. It then initializes a serializer instance with the professor_profile object.

#         Finally, it sends a GET request to the 'detail_professor' endpoint with the professor_profile ID as a parameter. It asserts that the response status code is 401 (Unauthorized), indicating that the user is anonymous.

#         Parameters:
#         - self: The instance of the test case class.

#         Returns:
#         - None

#         Raises:
#         - AssertionError: If the response status code is not 401 (Unauthorized).
#         """
#         client = APIClient()
#         user = baker.make(User)
#         college = baker.make(College)
#         field = baker.make(Field, college=college)
#         professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

#         serializer_instance = ProfessorProfileSerializer(professor_profile)

#         response = client.get(reverse('detail_professor', args=[professor_profile.id]), data = serializer_instance.data, format='json')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

#     def test_if_user_is_it_manager(self):
#         """
#         Test if the user is an IT manager.

#         This function performs a series of actions to test if the user is an IT manager. It creates a client object, a user object, a college object, a field object, and a professor profile object. Then, it creates an instance of the ProfessorProfileSerializer with the professor profile object. Finally, it makes a GET request to the 'detail_professor' endpoint, passing the professor profile ID as an argument and the 'json' format. It asserts that the response status code is equal to HTTP 200 OK.

#         Parameters:
#         - self: The instance of the class.

#         Returns:
#         - None
#         """
#         client = APIClient()
#         user = baker.make(User)
#         college = baker.make(College)
#         field = baker.make(Field, college=college)
#         professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

#         serializer_instance = ProfessorProfileSerializer(professor_profile)

#         response = client.get(reverse('detail_professor', args=[professor_profile.id]), format='json')

#         assert response.status_code == status.HTTP_200_OK, "Expected 200 OK status code"


# class TestProfessorList:
#     def test_if_user_is_anonymous(self):
#         """
#         Test if the user is anonymous.

#         This function creates an instance of `APIClient` to simulate an API client.
#         It then creates 10 instances of `ProfessorProfile` using the `baker.make` method.
#         These professor profiles are serialized using the `ProfessorProfileSerializer`.
#         A GET request is made to the `detail_professor` endpoint using the `client.get` method.
#         The expected status code of the response is `401 Unauthorized`.

#         Parameters:
#             self (TestClass): The current instance of the test class.

#         Returns:
#             None
#         """
#         client = APIClient()
#         professor_profiles = baker.make(ProfessorProfile, _quantity=10)

#         serializer_instance = ProfessorProfileSerializer(professor_profiles, many=True)

#         response = client.get(reverse('detail_professor'), format='json')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

#     def test_if_user_is_it_manager(self):
#         """
#         Test if the user is an IT manager.

#         This function creates a test client and makes a GET request to the 'detail_professor' endpoint.
#         It then checks if the response status code is equal to 200, indicating a successful request.

#         Parameters:
#         - self: The current instance of the test case.

#         Return:
#         - None
#         """
#         client = APIClient()
#         professor_profiles = baker.make(ProfessorProfile, _quantity=10)

#         serializer_instance = ProfessorProfileSerializer(professor_profiles, many=True)

#         response = client.get(reverse('detail_professor'), format='json')

#         assert response.status_code == status.HTTP_200_OK, "Expected 200 OK status code"


# class TestProfessorUpdate:
#     def test_if_user_is_anonymous(self):
#         """
#         Test if the user is anonymous.

#         This function creates a test environment by instantiating an APIClient and creating instances of User, College, Field, and ProfessorProfile using the baker library. It then creates an instance of ProfessorProfileSerializer with the created professor_profile object.

#         The function sends a PUT request to the 'update_professor' endpoint with the professor_profile id as an argument, and the serialized data from the serializer_instance object as the request's data. The format of the request data is set to 'json'.

#         The function asserts that the response's status code is equal to status.HTTP_401_UNAUTHORIZED, indicating that the user is not authorized. If the assertion fails, an AssertionError is raised with the message "Expected 401 Unauthorized status code".

#         This function does not take any parameters and does not return anything.
#         """
#         client = APIClient()
#         user = baker.make(User)
#         college = baker.make(College)
#         field = baker.make(Field, college=college)
#         professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

#         serializer_instance = ProfessorProfileSerializer(professor_profile)

#         response = client.put(reverse('update_professor', args=[professor_profile.id]), data=serializer_instance.data, format='json')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

#     def test_if_user_is_it_manager(self):
#         """
#         Function to test if a user is an IT manager.

#         Args:
#             self: The object itself.

#         Returns:
#             None
#         """
#         client = APIClient()
#         user = baker.make(User)
#         college = baker.make(College)
#         field = baker.make(Field, college=college)
#         professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

#         serializer_instance = ProfessorProfileSerializer(professor_profile)

#         response = client.put(reverse('update_professor', args=[professor_profile.id]), data=serializer_instance.data, format='json')

#         assert response.status_code == status.HTTP_205_RESET_CONTENT, "Expected 205 Reset Content status code"


# class TestProfessorDelete:
#     def test_if_user_is_anonymous(self):
#         """
#         Test if the user is anonymous.

#         This function creates a test client and sets up the necessary objects for testing. It then calls the API endpoint for deleting a professor profile with the given professor profile ID. The function asserts that the response status code is 401 UNAUTHORIZED, indicating that the user is not authenticated.

#         Parameters:
#             self (obj): The current instance of the test case.

#         Returns:
#             None
#         """

#         client = APIClient()
#         user = baker.make(User)
#         college = baker.make(College)
#         field = baker.make(Field, college=college)
#         professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

#         serializer_instance = ProfessorProfileSerializer(professor_profile)

#         response = client.delete(reverse('delete_professor', args=[professor_profile.id]), data=serializer_instance.data, format='json')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

#     def test_if_user_is_it_manager(self):
#         """
#         Test if the user is an IT manager.

#         This function creates a test scenario by instantiating various objects such as `client`, `user`, `college`, `field`, and `professor_profile`. It then creates an instance of the `ProfessorProfileSerializer` using the `professor_profile` object.

#         The function sends a DELETE request to the 'delete_professor' endpoint with the `professor_profile` ID as a path parameter and the serialized data as the request payload. The expected response status code is `204 No Content`.

#         Raises:
#             AssertionError: If the response status code is not `204 No Content`.

#         Parameters:
#             self (TestUserManager): The current instance of the test case.

#         Returns:
#             None
#         """
#         client = APIClient()
#         user = baker.make(User)
#         college = baker.make(College)
#         field = baker.make(Field, college=college)
#         professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

#         serializer_instance = ProfessorProfileSerializer(professor_profile)

#         response = client.delete(reverse('delete_professor', args=[professor_profile.id]), data=serializer_instance.data, format='json')

#         assert response.status_code == status.HTTP_204_NO_CONTENT, "Expected 204 No Content status code"






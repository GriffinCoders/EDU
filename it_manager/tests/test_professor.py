from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from account.models import User
from professor.models import ProfessorProfile
from common.models import College, Field
from professor.serializer import ProfessorProfileSerializer
import pytest
from model_bakery import baker

@pytest.mark.django_db
class TestProfessorCreation:
    def test_if_user_is_anonymous(self):
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
        client = APIClient()
        college = baker.make(College)
        field = baker.make(Field, college=college)
        professor_profile = baker.make(ProfessorProfile, college=college, field=field)

        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.post(reverse('create_professor'), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

    def test_if_user_is_not_authorized(self):
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
        client = APIClient()
        college = baker.make(College)
        field = baker.make(Field, college=college)
        professor_profile = baker.make(ProfessorProfile, college=college, field=field)

        client.force_authenticate(user=professor_profile.user)

        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.post(reverse('create_professor'), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_403_FORBIDDEN, "Expected 403 Forbidden status code"

    def test_correct_user_with_invalid_data(self):
        """
        Test case for checking if the function correctly handles the scenario where a user with invalid data is passed.

        This test case creates a test client and generates some test data using the `baker` library. It then creates a `ProfessorProfileSerializer` instance and modifies the `user` role to an invalid value. 

        The test client sends a POST request to the `create_professor` endpoint with the modified serializer data. The expected response status code is `400 Bad Request`.

        Raises:
            AssertionError: If the response status code is not `400 Bad Request`.

        Returns:
            None
        """
        client = APIClient()
        college = baker.make(College)
        field = baker.make(Field, college=college)
        professor_profile = baker.make(ProfessorProfile, college=college, field=field)

        serializer_instance = ProfessorProfileSerializer(professor_profile)
        serializer_instance.data['user']['role'] = '12'

        response = client.post(reverse('create_professor'), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST, "Expected 400 Bad Request status code"

    def test_correct_user_with_valid_data(self):
        """
        Test the scenario where a correct user with valid data is being processed.

        This test function creates instances of the required models using the `baker.make()` method.
        It then creates a serializer instance of the `ProfessorProfileSerializer` class using the
        created `professor_profile` object. 

        A POST request is made to the 'create_professor' endpoint of the API using the `client.post()`
        method. The data for the request is obtained from the `serializer_instance.data` attribute.
        The request is made in the 'json' format.

        The test asserts that the response status code is equal to `status.HTTP_201_CREATED`,
        indicating that the request was successful and a new resource was created.

        Raises:
            AssertionError: If the response status code is not `status.HTTP_201_CREATED`.

        """
        client = APIClient()
        user = baker.make(User)
        college = baker.make(College)
        field = baker.make(Field, college=college)
        professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.post(reverse('create_professor'), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_201_CREATED, "Expected 201 Created status code"


class TestProfessorRetrieve:
    def test_if_user_is_anonymous(self):
        """
        Test if the user is anonymous.

        This function creates a test environment by creating instances of various model classes such as User, College, Field, and ProfessorProfile. It then initializes a serializer instance with the professor_profile object.

        Finally, it sends a GET request to the 'detail_professor' endpoint with the professor_profile ID as a parameter. It asserts that the response status code is 401 (Unauthorized), indicating that the user is anonymous.

        Parameters:
        - self: The instance of the test case class.

        Returns:
        - None

        Raises:
        - AssertionError: If the response status code is not 401 (Unauthorized).
        """
        client = APIClient()
        user = baker.make(User)
        college = baker.make(College)
        field = baker.make(Field, college=college)
        professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.get(reverse('detail_professor', args=[professor_profile.id]), data = serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

    def test_if_user_is_it_manager(self):
        """
        Test if the user is an IT manager.

        This function performs a series of actions to test if the user is an IT manager. It creates a client object, a user object, a college object, a field object, and a professor profile object. Then, it creates an instance of the ProfessorProfileSerializer with the professor profile object. Finally, it makes a GET request to the 'detail_professor' endpoint, passing the professor profile ID as an argument and the 'json' format. It asserts that the response status code is equal to HTTP 200 OK.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        client = APIClient()
        user = baker.make(User)
        college = baker.make(College)
        field = baker.make(Field, college=college)
        professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.get(reverse('detail_professor', args=[professor_profile.id]), format='json')

        assert response.status_code == status.HTTP_200_OK, "Expected 200 OK status code"


class TestProfessorList:
    def test_if_user_is_anonymous(self):
        """
        Test if the user is anonymous.

        This function creates an instance of `APIClient` to simulate an API client.
        It then creates 10 instances of `ProfessorProfile` using the `baker.make` method.
        These professor profiles are serialized using the `ProfessorProfileSerializer`.
        A GET request is made to the `detail_professor` endpoint using the `client.get` method.
        The expected status code of the response is `401 Unauthorized`.

        Parameters:
            self (TestClass): The current instance of the test class.

        Returns:
            None
        """
        client = APIClient()
        professor_profiles = baker.make(ProfessorProfile, _quantity=10)

        serializer_instance = ProfessorProfileSerializer(professor_profiles, many=True)

        response = client.get(reverse('detail_professor'), format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

    def test_if_user_is_it_manager(self):
        """
        Test if the user is an IT manager.

        This function creates a test client and makes a GET request to the 'detail_professor' endpoint.
        It then checks if the response status code is equal to 200, indicating a successful request.

        Parameters:
        - self: The current instance of the test case.

        Return:
        - None
        """
        client = APIClient()
        professor_profiles = baker.make(ProfessorProfile, _quantity=10)

        serializer_instance = ProfessorProfileSerializer(professor_profiles, many=True)

        response = client.get(reverse('detail_professor'), format='json')

        assert response.status_code == status.HTTP_200_OK, "Expected 200 OK status code"


class TestProfessorUpdate:
    def test_if_user_is_anonymous(self):
        """
        Test if the user is anonymous.

        This function creates a test environment by instantiating an APIClient and creating instances of User, College, Field, and ProfessorProfile using the baker library. It then creates an instance of ProfessorProfileSerializer with the created professor_profile object.

        The function sends a PUT request to the 'update_professor' endpoint with the professor_profile id as an argument, and the serialized data from the serializer_instance object as the request's data. The format of the request data is set to 'json'.

        The function asserts that the response's status code is equal to status.HTTP_401_UNAUTHORIZED, indicating that the user is not authorized. If the assertion fails, an AssertionError is raised with the message "Expected 401 Unauthorized status code".

        This function does not take any parameters and does not return anything.
        """
        client = APIClient()
        user = baker.make(User)
        college = baker.make(College)
        field = baker.make(Field, college=college)
        professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.put(reverse('update_professor', args=[professor_profile.id]), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

    def test_if_user_is_it_manager(self):
        """
        Function to test if a user is an IT manager.

        Args:
            self: The object itself.

        Returns:
            None
        """
        client = APIClient()
        user = baker.make(User)
        college = baker.make(College)
        field = baker.make(Field, college=college)
        professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.put(reverse('update_professor', args=[professor_profile.id]), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_205_RESET_CONTENT, "Expected 205 Reset Content status code"


class TestProfessorDelete:
    def test_if_user_is_anonymous(self):
        """
        Test if the user is anonymous.

        This function creates a test client and sets up the necessary objects for testing. It then calls the API endpoint for deleting a professor profile with the given professor profile ID. The function asserts that the response status code is 401 UNAUTHORIZED, indicating that the user is not authenticated.

        Parameters:
            self (obj): The current instance of the test case.

        Returns:
            None
        """
        
        client = APIClient()
        user = baker.make(User)
        college = baker.make(College)
        field = baker.make(Field, college=college)
        professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.delete(reverse('delete_professor', args=[professor_profile.id]), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized status code"

    def test_if_user_is_it_manager(self):
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
        client = APIClient()
        user = baker.make(User)
        college = baker.make(College)
        field = baker.make(Field, college=college)
        professor_profile = baker.make(ProfessorProfile, user=user, college=college, field=field)

        serializer_instance = ProfessorProfileSerializer(professor_profile)

        response = client.delete(reverse('delete_professor', args=[professor_profile.id]), data=serializer_instance.data, format='json')

        assert response.status_code == status.HTTP_204_NO_CONTENT, "Expected 204 No Content status code"

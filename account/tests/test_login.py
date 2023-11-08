from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from account.models import User


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="login", password="login")

    def test_if_username_or_password_not_provided_return_400(self):
        response = self.client.post(reverse("account:login"), {
            "username": "test",
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse("account:login"), {
            "password": "test",
        })
        self.assertEqual(response.status_code, 400)

    def test_if_user_not_found_return_400(self):
        response = self.client.post(reverse("account:login"), {
            "username": "test",
            "password": "test"
        })
        self.assertEqual(response.status_code, 400)

    def test_if_user_is_found_return_200_and_valid_token(self):
        response = self.client.post(reverse("account:login"), {
            "username": "login",
            "password": "login"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data.get("token"))
        self.assertTrue(Token.objects.filter(user__username=self.user.username).exists())

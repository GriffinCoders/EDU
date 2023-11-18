from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

import pytest

from account.models import User


@pytest.mark.django_db
class LogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="logout", password="logout")

    def test_if_user_is_anonymous_returns_401(self):
        response = self.client.post(reverse("account:logout"))
        self.assertEqual(response.status_code, 401)

    def test_if_user_is_found_returns_204(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(reverse("account:logout"))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Token.objects.filter(user__username=self.user.username).exists())

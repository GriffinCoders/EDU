from django.urls import reverse
from django.core.cache import cache
from rest_framework.test import APITestCase

import pytest

from account.models import User


@pytest.mark.skip(reason="redis must configured in gitlab cli")
class ResetPasswordTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reset_password2",
                                             password="reset_password2",
                                             email="test@test.com")
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_if_email_not_found_return_400(self):
        response = self.client.post(reverse("account:reset-password"), {
            "email": "seethgwsergtbersg@test.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_if_email_found(self):
        # if email is valid returns 200
        response = self.client.post(reverse("account:reset-password"), {
            "email": self.user.email
        })
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(cache.get(self.user.email + "_otp", None))

        # if send duplicate otp returns 400
        response = self.client.post(reverse("account:reset-password"), {
            "email": self.user.email
        })
        self.assertEqual(response.status_code, 400)

        # if send email and not send new_password or otp returns 400
        response = self.client.post(reverse("account:reset-password"), {
            "email": self.user.email,
            "new_password": "new_password"
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse("account:reset-password"), {
            "email": self.user.email,
            "otp": 11111111111
        })
        self.assertEqual(response.status_code, 400)

        # if send email and new_password and otp is invalid returns 400
        response = self.client.post(reverse("account:reset-password"), {
            "email": self.user.email,
            "new_password": "new_password",
            "otp": 11111111111,
        })
        self.assertEqual(response.status_code, 400)

        # if email and otp and new_password is valid returns 200
        response = self.client.post(reverse("account:reset-password"), {
            "email": self.user.email,
            "new_password": "new_password",
            "otp": cache.get(self.user.email + "_otp", None),
        })
        self.assertEqual(response.status_code, 200)

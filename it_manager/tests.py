from django.test import TestCase
from rest_framework.test import APIClient
from account.models import User
from common.models import College, Field
from professor.models import ProfessorProfile


# Create your tests here.
class TestITManagerProfessor(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create('user1', 'testUser1', 'testUser1Password', 'fjytf@gmail.com ')
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile_pic', 'meli_code', 'gender', 'birth_date', 'role', 'created_at', 'updated_at']
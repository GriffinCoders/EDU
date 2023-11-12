# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
# from account.models import User
# from common.models import College, Field
# from professor.models import ProfessorProfile
# from account.factories import UserFactory
# from common.factories import CollegeFactory, FieldFactory
# from professor.factories import ProfessorProfileFactory
#
#
# class TestITManagerProfessor(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#
#         self.user1 = UserFactory()
#         self.college1 = CollegeFactory()
#         self.field1 = FieldFactory()
#         self.professor1 = ProfessorProfileFactory(user=self.user1, college=self.college1, field=self.field1)
#
#         self.user2 = UserFactory()
#         self.college2 = CollegeFactory()
#         self.field2 = FieldFactory()
#         self.professor2 = ProfessorProfileFactory(user=self.user2, college=self.college2, field=self.field2)
#
#         self.user3 = UserFactory()
#         self.college3 = CollegeFactory()
#         self.field3 = FieldFactory()
#         self.professor3 = ProfessorProfileFactory(user=self.user3, college=self.college3, field=self.field3)
#
#     def test_ListProfessorProfile(self):
#         response = self.client.get(reverse('list_professors'))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 3)
#
#     def test_CreateProfessorProfileView(self):
#         self.user4 = UserFactory()
#         data = {
#             'user': self.user4,
#             'college': self.college3.id,
#             'field': self.field3.id,
#             'orientation': 'test_orientation',
#             'order': 1
#         }
#         response = self.client.post(reverse('create_professor'), data)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(ProfessorProfile.objects.count(), 4)
#
#     def test_RetrieveProfessorProfileView(self):
#         response = self.client.get(reverse('detail_professor', args=[self.professor1.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['id'], self.professor1.id)
#         self.assertEqual(response.data['user']['id'], self.user1.id)
#         self.assertEqual(response.data['college']['id'], self.college1.id)
#         self.assertEqual(response.data['field']['id'], self.field1.id)
#
#     def test_UpdateProfessorProfileView(self):
#         data = {
#             'orientation': 'new_orientation',
#             'order': 2
#         }
#         response = self.client.put(reverse('update_professor', args=[self.professor1.id]), data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data['id'], self.professor1.id)
#         self.assertEqual(response.data['user']['id'], self.user1.id)
#         self.assertEqual(response.data['college']['id'], self.college1.id)
#         self.assertEqual(response.data['field']['id'], self.field1.id)
#         self.assertEqual(response.data['orientation'], 'new_orientation')
#         self.assertEqual(response.data['order'], 2)
#
#     def test_DeleteProfessorProfileView(self):
#         response = self.client.delete(reverse('delete_professor', args=[self.professor1.id]))
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(ProfessorProfile.objects.count(), 3)
#

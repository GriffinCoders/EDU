from bakery import Baker
from .models import ProfessorProfile
from account.factories import UserFactory
from common.factories import CollegeFactory, FieldFactory

baker = Baker()

class ProfessorProfileFactory(baker.Baker):
    class Meta:
        model = ProfessorProfile
        college = baker.subFactory(CollegeFactory)
        field = baker.subFactory(FieldFactory)
        user = baker.subFactory(UserFactory)
        orientation = 'test_orientation'
        order = 1

    @classmethod
    def _after_make(cls, professor_profile, create, values):
        if create:
            professor_profile.user = UserFactory.create()

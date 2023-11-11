from .models import ProfessorProfile
from account.factories import UserFactory
from common.factories import CollegeFactory, FieldFactory
from factory import Factory, SubFactory, Faker

class ProfessorProfileFactory(Factory):
    class Meta:
        model = ProfessorProfile

    user = SubFactory(UserFactory)
    college = SubFactory(CollegeFactory)
    field = SubFactory(FieldFactory)
    orientation = Faker('word')
    order = Faker('random_number')

# from .models import ProfessorProfile
# from account.factories import UserFactory
# from common.factories import CollegeFactory, FieldFactory
# from factory import Factory, SubFactory, Faker

# class ProfessorProfileFactory(Factory):
#     class Meta:
#         model = ProfessorProfile

#     user = SubFactory(UserFactory)
#     college = SubFactory(CollegeFactory)
#     field = SubFactory(FieldFactory)
#     orientation = Faker('word')
#     order = Faker('random_number')


# from model_bakery import baker


# class ProfessorProfileFactory:
#     @staticmethod
#     def create_professor_profile():
#         return baker.make('ProfessorProfile',
#                           user=baker.subfactory(UserFactory.create_user),
#                           college=baker.foreign_key(CollegeFactory.create_college),
#                           field=baker.foreign_key(FieldFactory.create_field),
#                           orientation=baker.Faker('word'),
#                           order=baker.Faker('word')
#                         )

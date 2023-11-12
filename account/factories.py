from factory import Factory, SubFactory, Faker
from .models import User  

# class UserFactory(Factory):
#     class Meta:
#         model = User

#     username = Faker('user_name')
#     first_name = Faker('first_name')
#     last_name = Faker('last_name')
#     email = Faker('email')
#     meli_code = Faker('random_number', digits=10)
#     gender = Faker('random_element', elements=('M', 'F'))
#     birth_date = Faker('date_of_birth')
#     role = Faker('random_element', elements=('0', '1', '2', '3'))


from model_bakery import baker
from account.models import User

class UserFactory:
    @staticmethod
    def create_user():
        return baker.make('User',
            username=baker.Faker('user_name'),
            first_name=baker.Faker('first_name'),
            last_name=baker.Faker('last_name'),
            email=baker.Faker('email'),
            meli_code=baker.Faker('random_number', digits=10),
            gender=baker.Faker('random_element', elements=('M', 'F')),
            birth_date=baker.Faker('date_of_birth'),
            role=baker.Faker('random_element', elements=('0', '1', '2', '3'))
        )


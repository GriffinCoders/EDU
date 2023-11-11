from factory import Factory, SubFactory, Faker
from .models import User  

class UserFactory(Factory):
    class Meta:
        model = User

    username = Faker('user_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    meli_code = Faker('random_number', digits=10)
    gender = Faker('random_element', elements=('M', 'F'))
    birth_date = Faker('date_of_birth')
    role = Faker('random_element', elements=('0', '1', '2', '3'))





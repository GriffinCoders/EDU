from model_bakery import baker
from professor.models import ProfessorProfile
from account.models import User
from common.models import College, Field

# College factory
collage_factory = baker.define('College', College, name=baker.Faker('company'))

# Field factory
field_factory = baker.define('Field', Field, 
    name=baker.Faker('word'),
    educational_group=baker.Faker('word'),
    college=baker.foreign_key('College'),
    units=baker.Faker('random_int', min=1, max=10),
    grade=baker.Faker('random_element', elements=('A', 'B', 'C'))
)

# User factory
user_factory = baker.define('User', User,
    username=baker.Faker('user_name'),
    first_name=baker.Faker('first_name'),
    last_name=baker.Faker('last_name'),
    email=baker.Faker('email'),
    meli_code=baker.Faker('random_number', digits=10),
    gender=baker.Faker('random_element', elements=('M', 'F')),
    birth_date=baker.Faker('date_of_birth'),
    role=baker.Faker('random_element', elements=('0', '1', '2', '3'))
)

# ProfessorProfile factory
ProfessorProfile_factory = baker.define('ProfessorProfile', ProfessorProfile,
    user=baker.subfactory('user_factory'),
    college=baker.foreign_key('College'),
    field=baker.foreign_key('Field'),
    orientation=baker.Faker('word'),
    order=baker.Faker('word')
)


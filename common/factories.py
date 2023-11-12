from factory import Factory, SubFactory, Faker
from .models import College, Field  
from .serializer import CollegeSerializer, FieldSerializer  
from model_bakery import baker

class CollegeFactory:
    @staticmethod
    def create_college():
        return baker.make('College', name=baker.Faker('company'))
    
class FieldFactory:
    @staticmethod
    def create_field():
        return baker.make('Field',
            name=baker.Faker('word'),
            educational_group=baker.Faker('word'),
            college=baker.foreign_key(CollegeFactory.create_college),
            units=baker.Faker('random_int', min=1, max=10),
            grade=baker.Faker('random_element', elements=('A', 'B', 'C'))
        )
from factory import Factory, SubFactory, Faker
from .models import College, Field  
from .serializer import CollegeSerializer, FieldSerializer  



class CollegeFactory(Factory):
    class Meta:
        model = College

    name = Faker('company')

class FieldFactory(Factory):
    class Meta:
        model = Field

    name = Faker('word')
    educational_group = Faker('word')
    college = SubFactory(CollegeFactory)
    units = Faker('random_number')
    grade = Faker('random_number')
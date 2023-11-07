from bakery import Baker
from .models import College, Field  
from .serializer import CollegeSerializer, FieldSerializer  

baker = Baker()

class CollageFactory(baker.Baker):
    class Meta:
        model = College  
        serializer = CollegeSerializer

class FieldFactory(baker.Baker):
    class Meta:
        model = Field  
        serializer = FieldSerializer
from bakery import baker
from .models import College, Field  
from .serializer import CollegeSerializer, FieldSerializer  



class CollageFactory(baker.Baker):
    class Meta:
        model = College  
        serializer = CollegeSerializer

class FieldFactory(baker.Baker):
    class Meta:
        model = Field  
        serializer = FieldSerializer
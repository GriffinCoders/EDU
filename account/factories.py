from bakery import baker
from .models import User  
from .serializer import UserSerializer  



class UserFactory(baker.Baker):
    class Meta:
        model = User  
        serializer = UserSerializer 
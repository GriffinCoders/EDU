from bakery import Baker
from .models import User  
from .serializer import UserSerializer  

baker = Baker()

class UserFactory(baker.Baker):
    class Meta:
        model = User  
        serializer = UserSerializer 
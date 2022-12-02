from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsUserProfileAndReadOnly
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

class UserInfo(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserProfileAndReadOnly]

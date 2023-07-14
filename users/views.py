from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serliazers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class UserPaymentsAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated] # только аутентифицированные пользователи имеют доступ к данному
    # представлению
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

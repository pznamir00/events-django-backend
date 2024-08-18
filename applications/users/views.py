from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer


class UserAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, **_):
        return self.request.user

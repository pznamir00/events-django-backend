from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer


class UserAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, **kargs):
        return self.request.user
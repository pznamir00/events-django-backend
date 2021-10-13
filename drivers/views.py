from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Platform
from .serializers import PlatformSerializer
from .permissions import IsAdminOrReadOnly


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly,)
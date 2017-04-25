from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import AdminOrReadOnly
import api.models as models
import api.serializers as serializers


class DistilleryList(generics.ListCreateAPIView):
    queryset = models.Distillery.objects.all()
    permission_classes = (AdminOrReadOnly, )
    serializer_class = serializers.DistillerySerializer
    pagination_class = LimitOffsetPagination

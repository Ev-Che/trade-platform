from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .models import Favorite, Inventory
from .serializers import FavoritesSerializer, InventorySerializer


class FavoritesViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):

    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class InventoryViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Inventory.objects.filter(user=self.request.user)

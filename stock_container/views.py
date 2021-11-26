from rest_framework import viewsets, mixins

from .models import Favorite, Inventory
from .serializers import FavoritesSerializer, InventorySerializer


class FavoritesViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = FavoritesSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class InventoryViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = InventorySerializer

    def get_queryset(self):
        return Inventory.objects.filter(user=self.request.user)

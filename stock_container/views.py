from rest_framework import viewsets, mixins

from .models import Favorite, Inventory
from . import serializers


class FavoritesViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    serializers = {
        'list': serializers.ListFavoritesSerializer,
        'create': serializers.CreateFavoritesSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related(
            'favorite_stock')


class InventoryViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    serializers = {
        'list': serializers.ListInventorySerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def get_queryset(self):
        queries = {
            'list': Inventory.objects.filter(
                user=self.request.user).select_related('stock'),
            'default': Inventory.objects.filter(user=self.request.user)
        }
        return queries.get(self.action, queries['default'])

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .db_queries import StockContainerDBManager
from .serializers import FavoritesSerializer, InventorySerializer


class FavoritesViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):

    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StockContainerDBManager.get_favorites(self.request.user)
        return queryset


class InventoryViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    serializer_class = InventorySerializer

    def get_queryset(self):
        queryset = StockContainerDBManager.get_user_inventory(
            self.request.user)
        return queryset

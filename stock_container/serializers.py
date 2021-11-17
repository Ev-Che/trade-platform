from rest_framework import serializers

from .models import Favorite, Inventory


class FavoritesSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Favorite
        fields = ['id', 'favorite_stock']


class InventorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'stock', 'quantity']

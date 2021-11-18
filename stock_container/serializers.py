from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Favorite, Inventory


class FavoritesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'favorite_stock']
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'favorite_stock']
            )
        ]


class InventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Inventory
        fields = ['id', 'stock', 'quantity']

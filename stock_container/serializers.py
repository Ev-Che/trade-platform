from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from stock_management.serializers import BaseStockSerializer
from .models import Favorite, Inventory

User = get_user_model()


class CreateFavoritesSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'favorite_stock')
        validators = [
            UniqueTogetherValidator(queryset=Favorite.objects.all(),
                                    fields=('user', 'favorite_stock'))
        ]


class ListFavoritesSerializer(serializers.ModelSerializer):
    favorite_stock = BaseStockSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'favorite_stock')


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'stock', 'quantity')
        validators = [
            UniqueTogetherValidator(queryset=Inventory.objects.all(),
                                    fields=('user', 'stock'))
        ]


class ListInventorySerializer(serializers.ModelSerializer):
    stock = BaseStockSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = ('id', 'stock', 'quantity')

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Favorite, Inventory

User = get_user_model()


class FavoritesSerializer(serializers.ModelSerializer):
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


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'stock', 'quantity')
        validators = [
            UniqueTogetherValidator(queryset=Inventory.objects.all(),
                                    fields=('user', 'stock'))
        ]

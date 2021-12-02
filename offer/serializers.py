from django.contrib.auth import get_user_model
from rest_framework import serializers

from stock_management.serializers import BaseStockSerializer
from .models import Offer
from .validators import OfferValidator

User = get_user_model()


class BaseOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('id', 'stock', 'user', 'is_active',)
        validators = [OfferValidator()]


class CreateUpdateOfferSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Offer
        fields = '__all__'
        validators = [OfferValidator()]


class ListOfferSerializer(serializers.ModelSerializer):
    stock = BaseStockSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = ('id', 'stock', 'user', 'order_type')


class DetailOfferSerializer(serializers.ModelSerializer):
    stock = BaseStockSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'

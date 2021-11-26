from rest_framework import serializers

from stock_management.serializers import BaseStockSerializer
from .models import Trade


class ListTradeSerializer(serializers.ModelSerializer):
    stock = BaseStockSerializer(read_only=True)

    class Meta:
        model = Trade
        fields = ('id', 'stock', 'seller', 'buyer', 'quantity', 'unit_price')


class DetailTradeSerializer(serializers.ModelSerializer):
    stock = BaseStockSerializer(read_only=True)

    class Meta:
        model = Trade
        fields = '__all__'

from rest_framework import serializers

from .models import Trade


class BaseTradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trade
        fields = ('id', 'stock', 'seller', 'buyer')


class DetailTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'

from rest_framework import serializers

from .models import Stock, Currency, Price


class PriceSerializer(serializers.ModelSerializer):
    currency = serializers.PrimaryKeyRelatedField(read_only=True,
                                                  source='currency.code')

    class Meta:
        model = Price
        fields = ['value', 'currency', 'date_of_change']


class StockSerializer(serializers.ModelSerializer):
    price = PriceSerializer()

    class Meta:
        model = Stock
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

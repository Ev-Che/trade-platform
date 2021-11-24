from rest_framework import serializers

from .models import Stock, Currency, Price


class BaseStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ('id', 'name')


class ListStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = ('id', 'name', 'code', 'price')


class DetailUpdateStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = '__all__'


class BaseCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('id', 'code')


class DetailUpdateCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class BasePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('id', 'currency', 'value')


class DetailUpdatePriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = '__all__'

from rest_framework import serializers

from .models import Stock, Currency, Price


# Currency serializers

class BaseCurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('id', 'code')


class ListCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'code')


class DetailCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class CreateUpdateCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


# Price serializers

class BasePriceSerializer(serializers.ModelSerializer):
    currency = BaseCurrencySerializer(read_only=True)

    class Meta:
        model = Price
        fields = ('id', 'value', 'currency')


class ListPriceSerializer(serializers.ModelSerializer):
    currency = BaseCurrencySerializer(read_only=True)

    class Meta:
        model = Price
        fields = ('id', 'value', 'currency')


class DetailPriceSerializer(serializers.ModelSerializer):
    currency = BaseCurrencySerializer(read_only=True)

    class Meta:
        model = Price
        fields = '__all__'


class CreateUpdatePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


# Stock serializers

class BaseStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ('id', 'name')


class ListStockSerializer(serializers.ModelSerializer):
    price = BasePriceSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = ('id', 'name', 'code', 'price')


class DetailStockSerializer(serializers.ModelSerializer):
    price = BasePriceSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'


class CreateUpdateStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

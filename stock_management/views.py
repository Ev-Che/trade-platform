from rest_framework import viewsets

from .models import Stock, Price, Currency
from .serializers import StockSerializer, PriceSerializer, CurrencySerializer


class StockViewSet(viewsets.ModelViewSet):
    serializer_class = StockSerializer
    queryset = Stock.objects.all()


class PriceViewSet(viewsets.ModelViewSet):
    serializer_class = PriceSerializer
    queryset = Price.objects.all()


class CurrencyViewSet(viewsets.ModelViewSet):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()

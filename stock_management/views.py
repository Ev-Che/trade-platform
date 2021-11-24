from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Stock, Price, Currency
from . import serializers


class MultiSerializerWithPermissionViewSet(viewsets.ModelViewSet):

    permissions = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'default': (IsAdminUser,),
    }

    serializers = {
        'default': None
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializers['default'])

    def get_permissions(self):
        permission_classes = self.permissions.get(self.action,
                                                  self.permissions['default'])
        return [permission() for permission in permission_classes]


class StockViewSet(MultiSerializerWithPermissionViewSet):
    queryset = Stock.objects.all()

    serializers = {
        'list': serializers.ListStockSerializer,
        'retrieve': serializers.DetailUpdateStockSerializer,
        'update': serializers.DetailUpdateStockSerializer,
        'partial_update': serializers.DetailUpdateStockSerializer,
        'default': serializers.BaseStockSerializer,
    }


class PriceViewSet(MultiSerializerWithPermissionViewSet):
    queryset = Price.objects.all()

    serializers = {
        'retrieve': serializers.DetailUpdatePriceSerializer,
        'update': serializers.DetailUpdatePriceSerializer,
        'partial_update': serializers.DetailUpdatePriceSerializer,
        'default': serializers.BasePriceSerializer,
    }


class CurrencyViewSet(MultiSerializerWithPermissionViewSet):
    queryset = Currency.objects.all()

    serializers = {
        'retrieve': serializers.DetailUpdateCurrencySerializer,
        'update': serializers.DetailUpdateCurrencySerializer,
        'partial_update': serializers.DetailUpdateCurrencySerializer,
        'default': serializers.BaseCurrencySerializer,
    }

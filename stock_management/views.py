from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Stock, Price, Currency
from . import serializers


class MultiSerializerWithPermissionViewSet(viewsets.ModelViewSet):
    permissions = {
        'create': (IsAdminUser,),
        'update': (IsAdminUser,),
        'partial_update': (IsAdminUser,),
        'destroy': (IsAdminUser,),
        'default': (IsAuthenticated,),
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

    serializers = {
        'list': serializers.ListStockSerializer,
        'retrieve': serializers.DetailStockSerializer,
        'create': serializers.CreateUpdateStockSerializer,
        'update': serializers.CreateUpdateStockSerializer,
        'partial_update': serializers.CreateUpdateStockSerializer,
        'default': serializers.BaseStockSerializer,
    }

    def get_queryset(self):
        queries = {
            'list': Stock.objects.all().select_related(
                'price', 'price__currency'),
            'retrieve': Stock.objects.all().select_related(
                'price', 'price__currency'),
            'default': Stock.objects.all()
        }
        return queries.get(self.action, queries['default'])


class PriceViewSet(MultiSerializerWithPermissionViewSet):

    serializers = {
        'list': serializers.ListPriceSerializer,
        'retrieve': serializers.DetailPriceSerializer,
        'create': serializers.CreateUpdatePriceSerializer,
        'update': serializers.CreateUpdatePriceSerializer,
        'partial_update': serializers.CreateUpdatePriceSerializer,
        'default': serializers.BasePriceSerializer,
    }

    def get_queryset(self):
        queries = {
            'list': Price.objects.all().select_related('currency'),
            'retrieve': Price.objects.all().select_related('currency'),
            'default': Price.objects.all()
        }
        return queries.get(self.action, queries['default'])


class CurrencyViewSet(MultiSerializerWithPermissionViewSet):
    queryset = Currency.objects.all()

    serializers = {
        'list': serializers.ListCurrencySerializer,
        'retrieve': serializers.DetailCurrencySerializer,
        'create': serializers.CreateUpdateCurrencySerializer,
        'update': serializers.CreateUpdateCurrencySerializer,
        'partial_update': serializers.CreateUpdateCurrencySerializer,
        'default': serializers.BaseCurrencySerializer,
    }

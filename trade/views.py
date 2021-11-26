from django.db.models import Q
from rest_framework import viewsets

from .models import Trade
from . import serializers


class TradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializers = {
        'list': serializers.ListTradeSerializer,
        'retrieve': serializers.DetailTradeSerializer,
    }

    def get_queryset(self):
        return Trade.objects.filter(Q(seller=self.request.user) |
                                    Q(buyer=self.request.user)).select_related(
            'stock')

    def get_serializer_class(self):
        return self.serializers.get(self.action)

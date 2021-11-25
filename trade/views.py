from django.db.models import Q
from rest_framework import viewsets

from .models import Trade
from .serializer import BaseTradeSerializer, DetailTradeSerializer


class TradeViewSet(viewsets.ReadOnlyModelViewSet):

    serializers = {
        'retrieve': DetailTradeSerializer,
        'default': BaseTradeSerializer
    }

    def get_queryset(self):
        return Trade.objects.filter(Q(seller=self.request.user) |
                                    Q(buyer=self.request.user))

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializers['default'])

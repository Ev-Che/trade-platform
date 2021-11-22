from django.db.models import Q
from rest_framework import viewsets

from .models import Trade
from .serializer import TradeSerializer


class TradeViewSet(viewsets.ModelViewSet):

    serializer_class = TradeSerializer

    def get_queryset(self):
        return Trade.objects.filter(Q(seller=self.request.user) |
                                    Q(buyer=self.request.user))


from rest_framework import viewsets

from .models import Stock
from .serializers import StockSerializer


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    """View for listing and retrieving stocks"""
    serializer_class = StockSerializer
    queryset = Stock.objects.all()

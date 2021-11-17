from rest_framework import viewsets

from .db_querries import StockDBManager
from .serializers import StockSerializer


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    """View for listing and retrieving stocks"""
    serializer_class = StockSerializer
    queryset = StockDBManager.get_all_stocks()

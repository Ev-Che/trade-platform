from rest_framework import views
from rest_framework.response import Response

from .services.trade_service import Trader


class TradeView(views.APIView):
    def get(self, request):
        Trader().make_a_trade()
        return Response({'status': 'ok'})

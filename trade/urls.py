from django.urls import path
from rest_framework import routers

# from trade.views import TradeViewSet
#
# router = routers.SimpleRouter()
# router.register('trades', TradeViewSet, basename='trades')

# urlpatterns = router.urls

from trade.views import TradeView

urlpatterns = [
    path('trades/', TradeView.as_view()),
]

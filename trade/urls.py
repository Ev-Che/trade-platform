from rest_framework import routers

from trade.views import TradeViewSet

router = routers.SimpleRouter()
router.register('trades', TradeViewSet, basename='trades')

urlpatterns = router.urls

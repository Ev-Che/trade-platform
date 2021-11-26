from rest_framework import routers

from .views import StockViewSet, CurrencyViewSet, PriceViewSet

router = routers.SimpleRouter()
router.register('stocks', StockViewSet, basename='stocks')
router.register('currencies', CurrencyViewSet, basename='prices')
router.register('prices', PriceViewSet, basename='currencies')

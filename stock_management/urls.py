from rest_framework import routers

from .views import StockViewSet, CurrencyViewSet, PriceViewSet

router = routers.SimpleRouter()
router.register('stocks', StockViewSet)
router.register('currencies', CurrencyViewSet)
router.register('prices', PriceViewSet)


urlpatterns = router.urls

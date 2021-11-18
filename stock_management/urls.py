from rest_framework import routers

from .views import StockViewSet

router = routers.SimpleRouter()
router.register('stocks', StockViewSet)

urlpatterns = router.urls

from rest_framework import routers

from .views import FavoritesViewSet, InventoryViewSet

router = routers.SimpleRouter()
router.register('favorites', FavoritesViewSet, basename='favorite')
router.register('inventory', InventoryViewSet, basename='inventory')

urlpatterns = router.urls

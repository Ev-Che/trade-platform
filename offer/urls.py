from rest_framework import routers

from .views import OfferViewSet

router = routers.SimpleRouter()
router.register('', OfferViewSet, basename='offers')

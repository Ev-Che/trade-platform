from django.contrib import admin
from django.urls import path, include

from offer.urls import router as offer_router
from stock_container.urls import router as stock_container_router
from stock_management.urls import router as stock_management_router
from trade.urls import router as trade_router

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Auth
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),

    # Apps
    path('api/offers/', include(offer_router.urls), name='offer'),
    path('api/container/', include(stock_container_router.urls),
         name='stock_container'),
    path('api/items/', include(stock_management_router.urls),
         name='stock_management'),
    path('api/trades/', include(trade_router.urls), name='trade'),
]

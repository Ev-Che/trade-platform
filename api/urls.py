from django.urls import path, include

urlpatterns = [
    # JWT Auth
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # Apps
    path('offers/', include('offer.urls'), name='offer'),
    path('container/', include('stock_container.urls'), name='stock_container'),
    path('items/', include('stock_management.urls'), name='stock_management'),
    path('trades/', include('trade.urls'), name='trade'),
]

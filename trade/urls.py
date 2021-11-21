from django.urls import path

from trade.views import TradeView

urlpatterns = [
    path('trades/', TradeView.as_view()),
]

from abc import ABC, abstractmethod
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from offer.models import Offer, SELL
from stock_management.models import Stock

User = get_user_model()


class OfferFinder(ABC):
    @abstractmethod
    def find_the_most_profitable(self) -> QuerySet:
        pass


class ProfitableOffersFinder(OfferFinder):

    def __init__(self, buy_offer: Offer):
        self.buy_offer = buy_offer

    def find_the_most_profitable(self):
        """Returns sell offers except exclude_user offers
        the price of which is less than max_price"""

        return self._get_sell_offers(exclude_user=self.buy_offer.user,
                                     stock=self.buy_offer.stock,
                                     max_price=self.buy_offer.price)

    @staticmethod
    def _get_sell_offers(exclude_user: User, stock: Stock,
                         max_price: Decimal) -> QuerySet:
        return (Offer.objects
                .filter(stock=stock, order_type=SELL, is_active=True,
                        price__lte=max_price)
                .exclude(user=exclude_user)
                .order_by('price'))

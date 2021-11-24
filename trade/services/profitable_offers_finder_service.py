from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from offer.models import Offer, SELL

User = get_user_model()


class ProfitableOffersFinder:

    def __init__(self, buy_offer: Offer):
        self.buy_offer = buy_offer

    def find_the_most_profitable(self) -> QuerySet:
        """Returns sell offers except exclude_user offers
        the price of which is less than max_price"""

        return self._get_sell_offers(exclude_user=self.buy_offer.user,
                                     max_price=self.buy_offer.price)

    @staticmethod
    def _get_sell_offers(exclude_user: User, max_price: Decimal) -> QuerySet:
        return (Offer.objects
                .filter(order_type=SELL, is_active=True, price__lte=max_price)
                .exclude(user=exclude_user)
                .order_by('price'))

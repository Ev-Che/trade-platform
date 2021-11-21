from offer.models import Offer, SELL
from ..models import Trade
from .profitable_offers_finder_service import ProfitableOffersFinder


class Trader:

    def make_a_trade(self):
        """Creates Trades with all objects from most_profitable list."""
        sell_offer = Offer.objects.filter(order_type=SELL,
                                          is_active=True).first()

        if sell_offer is not None:
            finder = ProfitableOffersFinder(sell_offer=sell_offer)
            most_profitable = finder.find_the_most_profitable()
            if most_profitable is not None:
                self._deal(buy_offers=most_profitable, sell_offer=sell_offer)

    def _deal(self, buy_offers: list[Offer], sell_offer: Offer):
        for offer in buy_offers:
            self._create_trade(buy_offer=offer, sell_offer=sell_offer)
            self._deactivate_offer(offer)

        self._deactivate_offer(sell_offer)

    def _create_trade(self, buy_offer: Offer, sell_offer: Offer):
        Trade.objects.create(stock=sell_offer.stock,
                             seller=sell_offer.user,
                             buyer=buy_offer.user,
                             quantity=buy_offer.entry_quantity,
                             unit_price=buy_offer.price,
                             buyer_offer=buy_offer,
                             seller_offer=sell_offer)

    def _deactivate_offer(self, offer: Offer):
        """Set is_active field=False in offer obj"""
        offer.is_active = False
        offer.save()

import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from offer.models import Offer, BUY
from stock_container.models import Inventory
from stock_management.models import Stock
from ..models import Trade
from .profitable_offers_finder_service import ProfitableOffersFinder
from loguru import logger

User = get_user_model()


class Trader:

    def make_a_trade(self) -> None:
        """Creates Trades."""

        buy_offer = self._get_random_buy_offer()
        logger.debug(f'buy offer: {buy_offer}')

        if buy_offer is not None:
            finder = ProfitableOffersFinder(buy_offer=buy_offer)
            most_profitable = finder.find_the_most_profitable()
            logger.debug(f'Most profitable: {most_profitable}')

            for sell_offer in most_profitable:
                self._deal(buy_offer=buy_offer, sell_offer=sell_offer)
                if not buy_offer.is_active:
                    break

    def _deal(self, buy_offer: Offer, sell_offer: Offer) -> None:
        """Creates a Trade between buy_offer and sell_offer.
        Add bought stocks to the buyer inventory.
        Remove sold stocks from the seller inventory"""

        trade = self._create_trade(buy_offer=buy_offer, sell_offer=sell_offer)

        self._add_stocks_to_the_inventory(
            user=buy_offer.user, stock=buy_offer.stock,
            quantity=trade.quantity)

        self._remove_stocks_from_the_inventory(
            user=sell_offer.user, stock=sell_offer.stock,
            quantity=trade.quantity)

    @staticmethod
    def _get_random_buy_offer() -> Offer:
        all_offers = Offer.objects.filter(order_type=BUY,
                                          is_active=True).select_related(
            'user', 'stock')

        return random.choice(tuple(all_offers)) if all_offers else None

    def _create_trade(self, buy_offer: Offer, sell_offer: Offer) -> Trade:
        """Reducing trading_quantity from offers.
        Created and returns Trade obj"""

        trading_quantity = self._get_trading_quantity(buy_offer=buy_offer,
                                                      sell_offer=sell_offer)

        self._reduce_the_quantity_in_offer(buy_offer, trading_quantity)
        self._reduce_the_quantity_in_offer(sell_offer, trading_quantity)

        return Trade.objects.create(stock=sell_offer.stock,
                                    seller=sell_offer.user,
                                    buyer=buy_offer.user,
                                    quantity=trading_quantity,
                                    unit_price=sell_offer.price,
                                    buyer_offer=buy_offer,
                                    seller_offer=sell_offer)

    @staticmethod
    def _get_trading_quantity(buy_offer: Offer, sell_offer: Offer) -> int:
        """Returns the quantity of stocks that can be used in trade"""

        if buy_offer.entry_quantity > sell_offer.entry_quantity:
            trading_quantity = sell_offer.entry_quantity
        else:
            trading_quantity = buy_offer.entry_quantity
        return trading_quantity

    @staticmethod
    def _add_stocks_to_the_inventory(user: User, stock: Stock,
                                     quantity: int) -> None:
        """Increase stocks quantity in the user inventory.
        If stock is not in the user inventory, creates a inventory"""

        try:
            inventory_obj = Inventory.objects.get(user=user, stock=stock)
            inventory_obj.quantity += quantity
            inventory_obj.save()
        except ObjectDoesNotExist:
            Inventory.objects.create(user=user, stock=stock, quantity=quantity)

    @staticmethod
    def _remove_stocks_from_the_inventory(user: User, stock: Stock,
                                          quantity: int) -> None:
        """Removes (quantity) of stocks from user inventory.
        If total quantity of stock in the user inventory = 0,
        then delete this inventory"""

        inventory_obj = Inventory.objects.get(user=user, stock=stock)

        inventory_obj.quantity -= quantity
        inventory_obj.save()

        if inventory_obj.quantity == 0:
            inventory_obj.delete()

    @staticmethod
    def _reduce_the_quantity_in_offer(offer: Offer,
                                      reducing_quantity: int) -> None:
        offer.entry_quantity -= reducing_quantity
        if offer.entry_quantity == 0:
            offer.is_active = False
        offer.save()

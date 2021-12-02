from django.contrib.auth import get_user_model

from offer.models import Offer, SELL
from stock_container.models import Inventory
from stock_management.models import Stock

User = get_user_model()


class SellOfferManager:

    @staticmethod
    def is_inventory_exists(user, stock):
        return Inventory.objects.filter(user=user, stock=stock).exists()

    @staticmethod
    def count_stocks_in_sell_offers(user: User, stock: Stock):
        stocks_in_different_sell_offers = 0
        for sell_offer in Offer.objects.filter(user=user,
                                               stock=stock,
                                               order_type=SELL,
                                               is_active=True):
            stocks_in_different_sell_offers += sell_offer.entry_quantity

        return stocks_in_different_sell_offers

    def are_there_enough_free_stocks(self, user: User, stock: Stock,
                                     entry_quantity: int):
        stocks_in_different_sell_offers = self.count_stocks_in_sell_offers(
            user=user, stock=stock)
        quantity_in_inventory = Inventory.objects.get(
            user=user, stock=stock).quantity

        return entry_quantity <= (quantity_in_inventory -
                                  stocks_in_different_sell_offers)

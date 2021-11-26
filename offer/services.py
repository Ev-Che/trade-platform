from django.contrib.auth import get_user_model

from offer.models import Offer, SELL
from stock_container.models import Inventory
from stock_management.models import Stock

User = get_user_model()


class SellOfferValidateManager:

    def __init__(self, user: User, stock: Stock, entry_quantity):
        self.user = user
        self.stock = stock
        self.entry_quantity = entry_quantity

    def is_inventory_exists(self):
        return Inventory.objects.filter(user=self.user,
                                        stock=self.stock).exists()

    def count_stocks_in_sell_offers(self):
        stocks_in_different_sell_offers = 0
        for sell_offer in Offer.objects.filter(user=self.user,
                                               stock=self.stock,
                                               order_type=SELL,
                                               is_active=True):
            stocks_in_different_sell_offers += sell_offer.entry_quantity

        return stocks_in_different_sell_offers

    def are_there_enough_free_stocks(self):
        stocks_in_different_sell_offers = self.count_stocks_in_sell_offers()
        quantity_in_inventory = Inventory.objects.get(
            user=self.user, stock=self.stock).quantity

        return self.entry_quantity <= (quantity_in_inventory -
                                       stocks_in_different_sell_offers)

from rest_framework import serializers

from .models import SELL
from .services import is_inventory_exists

WRONG_STOCK_MESSAGE = ('there is no such stock in the inventory '
                       'or there are not enough of them.')


class OfferValidator:
    def __init__(self, order_type, user, stock, entry_quantity):
        self.order_type = order_type
        self.user = user
        self.stock = stock
        self.entry_quantity = entry_quantity

    def _validate_selected_for_sale_stock(self):
        """Check that the stock selected for sale exists in the inventory
        and the quantity indicated for sale is less than that in the
        inventory"""

        if self.order_type == SELL:
            if not is_inventory_exists(user=self.user, stock=self.stock,
                                       quantity=self.entry_quantity):
                raise serializers.ValidationError(WRONG_STOCK_MESSAGE)

    def validate(self):
        self._validate_selected_for_sale_stock()

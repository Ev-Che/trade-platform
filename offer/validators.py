from rest_framework import serializers

from .models import SELL
from .services import is_inventory_exists

WRONG_STOCK_MESSAGE = ('there is no such stock in the inventory '
                       'or there are not enough of them.')


class OfferValidator:

    def __call__(self, value):
        self.order_type = value.get('order_type')
        self.user = value.get('user')
        self.stock = value.get('stock')
        self.entry_quantity = value.get('entry_quantity')

        self.validate()

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

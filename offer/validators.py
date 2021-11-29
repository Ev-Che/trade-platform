from django.contrib.auth import get_user_model
from rest_framework import serializers

from stock_management.models import Stock
from .models import SELL
from .services import SellOfferManager

WRONG_STOCK_MESSAGE = 'There is no such stock in the inventory.'
WRONG_QUANTITY_ERROR_MESSAGE = 'There is not enough stocks in the inventory'

User = get_user_model()


class OfferValidator:

    def __call__(self, value):
        self.order_type = value.get('order_type')
        self.user = value.get('user')
        self.stock = value.get('stock')
        self.entry_quantity = value.get('entry_quantity')

        self.validate()

    def validate(self):
        if self.order_type == SELL:
            self._validate_existence(user=self.user, stock=self.stock)
            self._validate_quantity(user=self.user, stock=self.stock,
                                    entry_quantity=self.entry_quantity)

    @staticmethod
    def _validate_existence(user: User, stock: Stock):
        """Check that the stock selected for sale exists in the inventory"""

        if not SellOfferManager.is_inventory_exists(user=user, stock=stock):
            raise serializers.ValidationError(WRONG_STOCK_MESSAGE)

    @staticmethod
    def _validate_quantity(user: User, stock: Stock, entry_quantity: int):
        """Checks that the quantity indicated for sale is less than that in the
        inventory + in other sell offers"""

        if not SellOfferManager().are_there_enough_free_stocks(
                user=user, stock=stock, entry_quantity=entry_quantity):
            raise serializers.ValidationError(WRONG_QUANTITY_ERROR_MESSAGE)

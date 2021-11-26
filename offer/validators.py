from rest_framework import serializers

from .models import SELL
from .services import SellOfferValidateManager

WRONG_STOCK_MESSAGE = 'There is no such stock in the inventory.'
WRONG_QUANTITY_ERROR_MESSAGE = 'There is not enough stocks in the inventory'


class OfferValidator:

    def __call__(self, value):
        self.order_type = value.get('order_type')
        self.user = value.get('user')
        self.stock = value.get('stock')
        self.entry_quantity = value.get('entry_quantity')

        self.validate()

    def validate(self):
        if self.order_type == SELL:
            validate_manager = SellOfferValidateManager(
                user=self.user, stock=self.stock,
                entry_quantity=self.entry_quantity)
            self._validate_existence(validate_manager)
            self._validate_quantity(validate_manager)

    @staticmethod
    def _validate_existence(validate_manager: SellOfferValidateManager):
        """Check that the stock selected for sale exists in the inventory"""

        if not validate_manager.is_inventory_exists():
            raise serializers.ValidationError(WRONG_STOCK_MESSAGE)

    @staticmethod
    def _validate_quantity(validate_manager: SellOfferValidateManager):
        """Checks that the quantity indicated for sale is less than that in the
        inventory + in other sell offers"""

        if not validate_manager.are_there_enough_free_stocks():
            raise serializers.ValidationError(WRONG_QUANTITY_ERROR_MESSAGE)

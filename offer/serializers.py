from rest_framework import serializers

from .models import Offer, SELL, WRONG_STOCK_MESSAGE
from .services import is_inventory_exists


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = '__all__'

    # def validate(self, attrs):
    #     """check that the stock selected for sale exists in the inventory
    #     and the quantity indicated for sale is less than that in the
    #     inventory"""
    #
    #     if attrs['order_type'] == SELL:
    #         if not is_inventory_exists(attrs['user'], attrs['stock'],
    #                                    attrs['entry_quantity']):
    #             raise serializers.ValidationError(WRONG_STOCK_MESSAGE)
    #
    #     return attrs

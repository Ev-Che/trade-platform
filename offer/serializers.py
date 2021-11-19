from rest_framework import serializers

from .models import Offer
from .validators import OfferValidator


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = '__all__'

    def validate(self, attrs):
        validator = OfferValidator(order_type=attrs['order_type'],
                                   user=attrs['user'], stock=attrs['stock'],
                                   entry_quantity=attrs['entry_quantity'])
        validator.validate()

        return attrs

from rest_framework import serializers

from .models import Offer
from .validators import OfferValidator


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = '__all__'
        validators = [OfferValidator()]

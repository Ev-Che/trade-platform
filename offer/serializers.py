from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Offer
from .validators import OfferValidator

User = get_user_model()


class BaseOfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('id', 'stock', 'user', 'is_active',)
        validators = [OfferValidator()]


class CreateUpdateDetailOfferSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(default=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Offer
        fields = '__all__'
        validators = [OfferValidator()]

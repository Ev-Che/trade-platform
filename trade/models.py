from django.contrib.auth import get_user_model
from django.db import models

from offer.models import Offer
from stock_management.models import Stock

User = get_user_model()


class Trade(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='seller_trade',
                               related_query_name='seller_trade')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='buyer_trade',
                              related_query_name='buyer_trade')
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    seller_offer = models.ForeignKey(Offer, on_delete=models.CASCADE,
                                     related_name='seller_offer',
                                     related_query_name='seller_offer')
    buyer_offer = models.ForeignKey(Offer, on_delete=models.CASCADE,
                                    related_name='buyer_offer',
                                    related_query_name='buyer_offer')

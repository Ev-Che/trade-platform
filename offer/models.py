from django.contrib.auth import get_user_model
from django.db import models

from stock_management.models import Stock

User = get_user_model()

BUY = 'B'
SELL = 'S'

ORDER_TYPE_CHOICES = [
    (BUY, 'Buy'),
    (SELL, 'Sell'),
]


class Offer(models.Model):
    # stock = models.ForeignKey('Inventory', on_delete=models.SET_NULL,
    #                           blank=True, null=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE,
                              blank=True, null=False)
    entry_quantity = models.IntegerField('Entry quantity')
    order_type = models.CharField(max_length=1, choices=ORDER_TYPE_CHOICES)
    price = models.DecimalField('Price', max_digits=7, decimal_places=2)
    is_active = models.BooleanField('Is active')

    def save(self, *args, **kwargs):
        if self.order_type == BUY:
            pass
        elif self.order_type == SELL:
            print('sell')

        super().save(*args, **kwargs)

from django.contrib.auth import get_user_model
from django.db import models

from stock_container.models import Inventory
from stock_management.models import Stock

User = get_user_model()

BUY = 'B'
SELL = 'S'


class Offer(models.Model):
    class OrderTypeChoices(models.TextChoices):
        buy = BUY, 'Buy'
        sell = SELL, 'Sell'

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_quantity = models.PositiveIntegerField('Entry quantity')
    order_type = models.CharField(max_length=1,
                                  choices=OrderTypeChoices.choices)
    price = models.DecimalField('Price', max_digits=7, decimal_places=2)
    is_active = models.BooleanField('Is active', default=True)

    def __str__(self):
        return (f'{self.__class__.__name__}({self.stock.code}) '
                f'price {self.price}')

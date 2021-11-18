from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .services import is_inventory_exists
from stock_container.models import Inventory
from stock_management.models import Stock

User = get_user_model()

WRONG_STOCK_MESSAGE = 'there is no such stock in the inventory ' \
                      'or there are not enough of them.'

BUY = 'B'
SELL = 'S'

ORDER_TYPE_CHOICES = [
    (BUY, 'Buy'),
    (SELL, 'Sell'),
]


class Offer(models.Model):

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_quantity = models.IntegerField('Entry quantity')
    order_type = models.CharField(max_length=1, choices=ORDER_TYPE_CHOICES)
    price = models.DecimalField('Price', max_digits=7, decimal_places=2)
    is_active = models.BooleanField('Is active', default=True)

    def clean(self):
        if self.order_type == SELL:
            if not is_inventory_exists(user=self.user, stock=self.stock,
                                       quantity=self.entry_quantity):
                raise ValidationError({'stock': _(WRONG_STOCK_MESSAGE)})

    def __str__(self):
        return f'{self.__class__.__name__}({self.stock.code})'

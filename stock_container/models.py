from django.contrib.auth import get_user_model
from django.db import models

from stock_management.models import Stock

User = get_user_model()


class Favorites(models.Model):
    """User favorites stocks"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites_stocks = models.ForeignKey(Stock, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['user', 'favorites_stocks']]

    def __str__(self):
        return f'{self.user.name} {self.__class__.__name__}'


class Inventory(models.Model):
    """User stocks"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stocks = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.user.name} {self.__class__.__name__}'

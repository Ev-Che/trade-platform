from django.contrib.auth import get_user_model
from django.db import models

from stock_management.models import Stock

User = get_user_model()


class Favorite(models.Model):
    """User favorites stocks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'favorite_stock',)

    def __str__(self):
        return f'{self.user.username} {self.__class__.__name__}'


class Inventory(models.Model):
    """User stocks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f'{self.user.username} {self.__class__.__name__}'

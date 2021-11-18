from django.db import models


class StockBase(models.Model):
    code = models.CharField('Code', max_length=8, unique=True)
    name = models.CharField('Name', max_length=128, unique=True)

    class Meta:
        abstract = True


class Currency(StockBase):

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.code


class Stock(StockBase):
    """Specific stock model"""
    price = models.OneToOneField('Price', on_delete=models.CASCADE,
                                 related_name='price')
    details = models.TextField('Details', blank=True, null=True,
                               max_length=512)

    def __str__(self):
        return f'{self.__class__.__name__}({self.code})'


class Price(models.Model):
    """Price of specific stock"""
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    value = models.DecimalField('Value', max_digits=7, decimal_places=2,
                                blank=True, null=True)
    date_of_change = models.DateTimeField('Date of change')

    def __str__(self):
        return f'{self.__class__.__name__} {self.value}{self.currency.code}'

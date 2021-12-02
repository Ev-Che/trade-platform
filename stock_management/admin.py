from django.contrib import admin

from stock_management.models import Stock, Price, Currency

admin.site.register(Stock)
admin.site.register(Price)
admin.site.register(Currency)

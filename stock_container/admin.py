from django.contrib import admin

from stock_container.models import Favorite, Inventory

admin.site.register(Favorite)
admin.site.register(Inventory)

from django.contrib import admin

from stock_container.models import Favorites, Inventory

admin.site.register(Favorites)
admin.site.register(Inventory)

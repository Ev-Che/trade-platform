from .models import Favorite, Inventory


class StockContainerDBManager:

    @staticmethod
    def get_favorites(user):
        return Favorite.objects.filter(user=user)

    @staticmethod
    def get_user_inventory(user):
        return Inventory.objects.filter(user=user)

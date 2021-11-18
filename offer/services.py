from stock_container.models import Inventory


def is_inventory_exists(user, stock, quantity):
    return Inventory.objects.filter(user=user, stock=stock,
                                    quantity__gte=quantity).exists()

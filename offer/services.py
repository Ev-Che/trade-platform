from offer.models import Offer, SELL
from stock_container.models import Inventory


def is_inventory_exists(user, stock):
    return Inventory.objects.filter(user=user, stock=stock).exists()


def count_stocks_in_sell_offers(user, stock):
    stocks_in_different_sell_offers = 0

    for sell_offer in Offer.objects.filter(user=user, stock=stock,
                                           order_type=SELL, is_active=True):
        stocks_in_different_sell_offers += sell_offer.entry_quantity

    return stocks_in_different_sell_offers


def are_there_enough_free_stocks(user, stock, entry_quantity):
    stocks_in_different_sell_offers = count_stocks_in_sell_offers(
        user=user, stock=stock)

    quantity_in_inventory = Inventory.objects.get(
        user=user, stock=stock).quantity

    return entry_quantity <= (quantity_in_inventory -
                              stocks_in_different_sell_offers)

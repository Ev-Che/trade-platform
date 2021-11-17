from .models import Stock, Price


class StockDBManager:

    @staticmethod
    def get_all_stocks():
        return Stock.objects.all()

    @staticmethod
    def get_price():
        Price.objects.all()

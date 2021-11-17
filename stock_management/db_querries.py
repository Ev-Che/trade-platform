from .models import Stock, Price


class StockDBManager:

    @staticmethod
    def get_all_stocks():
        return Stock.objects.all()

    @staticmethod
    def get_stock_by_id(stock_id):
        return Stock.objects.get(id=stock_id)

    @staticmethod
    def get_price():
        Price.objects.all()

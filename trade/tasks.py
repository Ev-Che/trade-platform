from trade.services.trade_service import Trader
from trade_platform.celery import app


@app.task
def make_a_trade_task():
    print('Start task')
    Trader().make_a_trade()
    print('Finish task')

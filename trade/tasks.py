from datetime import timedelta

from celery.task import periodic_task
from celery.utils.log import get_task_logger

from trade.services.trade_service import Trader

logger = get_task_logger(__name__)


@periodic_task(run_every=timedelta(minutes=0.5))
def make_a_trade_task():
    logger.info('Start task')
    Trader().make_a_trade()
    logger.info('Finish task')

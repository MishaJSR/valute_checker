import logging

import uvicorn
from fastapi import FastAPI
from rates_router.router import router as rates_router
import betterlogging as bl
from apscheduler.schedulers.background import BackgroundScheduler

from tasks.update_info import update_info
from base_config import settings


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=log_level,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting server")


setup_logging()
url = settings.get_url()
app = FastAPI(title="Valute App")
scheduler = BackgroundScheduler()
scheduler.add_job(update_info, 'cron', hour=11, minute=00, args=[url])
scheduler.start()
app.include_router(rates_router)


if __name__ == "__main__":
    update_info(settings.get_url())
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
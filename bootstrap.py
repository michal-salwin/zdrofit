from kink import di
from log.Logger import Logger
from app_config.AppConfig import AppConfig

def bootstrap_di() -> None:
    logger = Logger('scrapper.log')
    app_config = AppConfig('scrapper.ini')

    di[Logger] = logger
    di[AppConfig] = app_config


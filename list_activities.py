from ZdrofitScrapper import ZdrofitScrapper
from app_logger.AppLogger import AppLogger
from app_config.AppConfig import AppConfig
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--initials",     required=True, help="Athlete initials - first letters of name and surname")
ap.add_argument("-c", "--club_name",    required=True, help="Club name")

args = vars(ap.parse_args())

logger = AppLogger()
config = AppConfig()
scrapper = ZdrofitScrapper(args['initials'], config, logger)
scrapper.get_activities(args['club_name'])


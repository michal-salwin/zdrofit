from ZdrofitScrapper import ZdrofitScrapper
from app_logger.AppLogger import AppLogger
from app_config.AppConfig import AppConfig
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--initials",     required=True, help="Athlete initials - first letters of name and surname")
ap.add_argument("-c", "--club_name",    required=True, help="Club name")
ap.add_argument("-a", "--activity",     required=True, help="Activity name")
ap.add_argument("-w", "--weekday",      required=True, help="Activity weekday")
ap.add_argument("-s", "--start_hour",   required=True, help="Activity start hour")

args = vars(ap.parse_args())

logger = AppLogger()
config = AppConfig()
scrapper = ZdrofitScrapper(args['initials'], config, logger)

scrapper.book_activity(args['club_name'],args['activity'],weekday=args['weekday'], hour=args['start_hour'])


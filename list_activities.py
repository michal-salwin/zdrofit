from app_logger.AppLogger import AppLogger
from app_config.AppConfig import AppConfig
import argparse

from zdrofit.Booker import Booker

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--initials",     required=True, help="Athlete initials - first letters of name and surname")
ap.add_argument("-c", "--club_name",    required=True, help="Club name")

args = vars(ap.parse_args())

logger = AppLogger()
config = AppConfig()
booker = Booker(args['initials'], config, logger)
booker.get_activities(args['club_name'])

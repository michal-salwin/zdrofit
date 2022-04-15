from app_logger.AppLogger import AppLogger
from app_config.AppConfig import AppConfig
import argparse

from zdrofit.Booker import Booker
from zdrofit.Club import Club
from zdrofit.User import User

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--initials",     required=True, help="Athlete initials - first letters of name and surname")
ap.add_argument("-c", "--club_name",    required=True, help="Club name")

args = vars(ap.parse_args())

logger = AppLogger()
config = AppConfig()
club = Club(args['club_name'])
user = User(args['initials'], config)

booker = Booker(user, logger)
booker.get_activities(club)


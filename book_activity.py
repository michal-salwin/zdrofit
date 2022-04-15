from zdrofit.Activity import Activity
from zdrofit.Booker import Booker
from app_logger.AppLogger import AppLogger
from app_config.AppConfig import AppConfig

import argparse
from zdrofit.Club import Club

from zdrofit.User import User

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--initials",     required=True, help="Athlete initials - first letters of name and surname")
ap.add_argument("-c", "--club_name",    required=True, help="Club name")
ap.add_argument("-a", "--activity",     required=True, help="Activity name")
ap.add_argument("-w", "--weekday",      required=True, help="Activity weekday")
ap.add_argument("-s", "--start_hour",   required=True, help="Activity start hour")

args = vars(ap.parse_args())

logger = AppLogger()
config = AppConfig()
activity = Activity()
user = User(args['initials'], config)

activity.club = Club(args['club_name'])
activity.name = args['activity']
activity.weekday = args['weekday']
activity.hour = args['start_hour']

booker = Booker(user, logger)
booker.book_activity(activity)


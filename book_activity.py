from booker.Activity import Activity
from booker.Booker import Booker
from app_config.AppConfig import AppConfig

import argparse
from booker.Club import Club
from booker.GymOperator import GymOperator

from booker.User import User
from booker.activity_list_builder.ZdrofitActivityListBuilder import ZdrofitActivityListBuilder
from booker.rest_interface.ZdrofitRestInterface import ZdrofitRestInterface

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--initials",       required=True, help="Athlete initials - first letters of name and surname")
ap.add_argument("-g", "--gym_operator",   required=True, help="Gym operator (zdrofit/other_gym")
ap.add_argument("-c", "--club_name",      required=True, help="Club name")
ap.add_argument("-a", "--activity",       required=True, help="Activity name")
ap.add_argument("-w", "--weekday",        required=True, help="Activity weekday")
ap.add_argument("-s", "--start_hour",     required=True, help="Activity start hour")

args = vars(ap.parse_args())

config = AppConfig()
activity = Activity()
user = User(args['initials'], config)
club = Club(args['club_name'])
gym_operator = GymOperator('gym_operator')
activity.club = club
activity.name = args['activity']
activity.weekday = args['weekday']
activity.hour = args['start_hour']

booker = Booker(user, ZdrofitRestInterface(), ZdrofitActivityListBuilder())
booker.book_activity(activity)


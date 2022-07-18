from booker.Activity import Activity
from booker.Booker import Booker
from app_config.AppConfig import AppConfig

import argparse
from booker.activity_list.ActivityListBuilderFactory import ActivityListBuilderFactory
from booker.club.ClubFactory import ClubFactory
from booker.User import User
from booker.rest_interface.RestInterfaceFactory import RestInterfaceFactory

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--initials",       required=True, help="Athlete initials - first letters of name and surname")
ap.add_argument("-c", "--club_name",      required=True, help="Club name")
ap.add_argument("-a", "--activity",       required=True, help="Activity name")
ap.add_argument("-w", "--weekday",        required=True, help="Activity weekday")
ap.add_argument("-s", "--start_hour",     required=True, help="Activity start hour")

args = vars(ap.parse_args())

config = AppConfig()
gym_operator = config.get_account_param(args['initials'],'gym_operator')
activity = Activity()
user = User(args['initials'], config)
club = ClubFactory (gym_operator,args['club_name']).get_club()

activity.club = club
activity.name = args['activity']
activity.weekday = args['weekday']
activity.hour = args['start_hour']

booker = Booker(user, RestInterfaceFactory(gym_operator).get_instance(), ActivityListBuilderFactory(gym_operator).get_instance())
booker.book_activity(activity)


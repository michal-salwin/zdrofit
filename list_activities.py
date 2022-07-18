from app_config.AppConfig import AppConfig
import argparse

from booker.Booker import Booker
from booker.activity_list.ActivityListBuilderFactory import ActivityListBuilderFactory
from booker.club.ClubFactory import ClubFactory
from booker.User import User
from booker.rest_interface.RestInterfaceFactory import RestInterfaceFactory

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--initials",       required=True, help="Athlete initials - name and surname first letters")
ap.add_argument("-c", "--club_name",      required=True, help="Club name")

args = vars(ap.parse_args())

config = AppConfig()
gym_operator = config.get_account_param(args['initials'],'gym_operator')
club = ClubFactory (gym_operator,args['club_name']).get_club()
user = User(args['initials'], config)

booker = Booker(user, RestInterfaceFactory(gym_operator).get_instance(), ActivityListBuilderFactory(gym_operator).get_instance())

booker.get_activities(club)


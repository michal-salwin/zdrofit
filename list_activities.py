from app_config.AppConfig import AppConfig
import argparse

from booker.Booker import Booker
from booker.activity_list.ActivityListBuilder import ActivityListBuilder
from booker.club.ClubBuilder import ClubBuilder
from booker.User import User
from booker.rest_interface.RestInterfaceBuilder import RestInterfaceBuilder

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--initials",       required=True, help="Athlete initials - name and surname first letters")
ap.add_argument("-c", "--club_name",      required=True, help="Club name")

args = vars(ap.parse_args())

config = AppConfig()
gym_operator = config.get_account_param(args['initials'],'gym_operator')
club = ClubBuilder (gym_operator,args['club_name']).get_club()
user = User(args['initials'], config)

booker = Booker(user, RestInterfaceBuilder(gym_operator).get_instance(), ActivityListBuilder(gym_operator).get_instance())

booker.get_activities(club)


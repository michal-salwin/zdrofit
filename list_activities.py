from app_config.AppConfig import AppConfig
import argparse

from booker.Booker import Booker
from booker.Club import Club
from booker.GymOperator import GymOperator
from booker.User import User
from booker.activity_list_builder.ZdrofitActivityListBuilder import ZdrofitActivityListBuilder
from booker.rest_interface.ZdrofitRestInterface import ZdrofitRestInterface

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--initials",       required=True, help="Athlete initials - name and surname first letters")
ap.add_argument("-g", "--gym_operator",   required=True, help="Gym operator (zdrofit/other_gym")
ap.add_argument("-c", "--club_name",      required=True, help="Club name")

args = vars(ap.parse_args())

config = AppConfig()
club = Club(args['club_name'])
gym_operator = GymOperator('gym_operator')
user = User(args['initials'], config)

booker = Booker(user, ZdrofitRestInterface(), ZdrofitActivityListBuilder())
booker.get_activities(club)


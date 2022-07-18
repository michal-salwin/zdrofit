from booker.club.CityFitClub import CityFitClub
from booker.club.Club import Club
from booker.club.ZdrofitClub import ZdrofitClub


class ClubFactory:

    __gym_operator: str
    __club_name: str
    
    def __init__(self, gym_operator: str, club_name: str):
        self.__gym_operator = gym_operator
        self.__club_name = club_name
    
    def get_club(self) -> Club:
        match self.__gym_operator:
            case 'zdrofit':
                return ZdrofitClub(self.__club_name)
            case 'cityfit':
                return CityFitClub(self.__club_name)

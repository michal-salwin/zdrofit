from booker.rest_interface.GymRestInterface import GymRestInterface
from booker.rest_interface.ZdrofitRestInterface import ZdrofitRestInterface
from booker.rest_interface.CityFitRestInterface import CityFitRestInterface

class RestInterfaceFactory:

    __gym_operator: str
    
    def __init__(self, gym_operator: str):
        self.__gym_operator = gym_operator
    
    def get_instance(self) -> GymRestInterface:
        match self.__gym_operator:
            case 'zdrofit':
                return ZdrofitRestInterface()
            case 'cityfit':
                return CityFitRestInterface()
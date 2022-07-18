from booker.activity_list.ActivityListBuilder import ActivityListBuilder
from booker.activity_list.CityFitActivityListBuilder import CityFitActivityListBuilder
from booker.activity_list.ZdrofitActivityListBuilder import ZdrofitActivityListBuilder

class ActivityListBuilderFactory:

    __gym_operator: str
    
    def __init__(self, gym_operator: str):
        self.__gym_operator = gym_operator
    
    def get_instance(self) -> ActivityListBuilder:
        match self.__gym_operator:
            case 'zdrofit':
                return ZdrofitActivityListBuilder()
            case 'cityfit':
                return CityFitActivityListBuilder()
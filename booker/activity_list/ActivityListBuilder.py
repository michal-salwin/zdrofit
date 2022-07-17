from booker.activity_list.ActivityList import ActivityList
from booker.activity_list.CityFitActivityList import CityFitActivityList
from booker.activity_list.ZdrofitActivityList import ZdrofitActivityList

class ActivityListBuilder:

    __gym_operator: str
    
    def __init__(self, gym_operator: str):
        self.__gym_operator = gym_operator
    
    def get_instance(self) -> ActivityList:
        match self.__gym_operator:
            case 'zdrofit':
                return ZdrofitActivityList()
            case 'cityfit':
                return CityFitActivityList()
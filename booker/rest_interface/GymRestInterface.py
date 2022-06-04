from abc import ABC, abstractmethod
from booker.Club import Club
from booker.rest_interface.BaseRequest import BaseRequest

class GymRestInterface(ABC):

    request: BaseRequest

    def __init__(self):
        self.request = BaseRequest()
 
    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def get_weekly_classes(self, club: Club) -> str:
        pass
 
    @abstractmethod
    def book_class(self,class_id):
        pass

    @abstractmethod
    def cancel_booking(self,class_id):
        pass


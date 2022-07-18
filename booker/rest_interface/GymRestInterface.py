from abc import ABC, abstractmethod
from booker.Activity import Activity
from booker.User import User
from booker.club.Club import Club
from booker.rest_interface.BaseRequest import BaseRequest

class GymRestInterface(ABC):

    request: BaseRequest

    def __init__(self):
        self.request = BaseRequest()
 
    @abstractmethod
    def login(self, user: User):
        pass

    @abstractmethod
    def get_weekly_classes(self, club: Club) -> str:
        pass
 
    @abstractmethod
    def book_class(self,activity: Activity):
        pass

    @abstractmethod
    def cancel_booking(self,activity: Activity):
        pass


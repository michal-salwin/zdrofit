from booker.Activity import Activity
from booker.User import User
from booker.rest_interface.GymRestInterface import GymRestInterface
from exceptions.HttpRequestError import HttpRequestError
from booker.club.Club import Club

class ZdrofitRestInterface(GymRestInterface):


    def __init__(self):
        super().__init__()
        self.request.base_url = 'https://zdrofit.perfectgym.pl/'

    
    def login(self, user: User):
        data = {
            "RememberMe": "false",
            "Login": user.get_login(),
            "Password": user.get_password()
        }  

        uri = '/ClientPortal2/Auth/Login' 
        response = self.request.login(uri, data=data)

        if response.status_code != 200:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)


    def get_weekly_classes(self, club: Club) -> str:
        data = {
            "clubId": club.get_id(),
            "categoryId": 'null',
            "daysInWeek": '7'
        }
        uri = '/ClientPortal2/Classes/ClassCalendar/WeeklyClasses'
        response = self.request.post(uri, data=data)
        if response.status_code != 200:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)
 
        return response.text

 
    def book_class(self,activity: Activity):
        data = {
            "classId": activity.id
        }
        uri = '/ClientPortal2/Classes/ClassCalendar/BookClass'
        
        response = self.request.post(uri, data=data)

        if response.status_code != 200:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)

    def cancel_booking(self,activity: Activity):
        data = {
            "classId": activity.id
        }
        uri = '/ClientPortal2/Classes/ClassCalendar/CancelBooking'
        
        response = self.request.post(uri, data=data)
        if response.status_code != 200:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)


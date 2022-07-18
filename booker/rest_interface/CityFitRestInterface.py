from booker.Activity import Activity
from booker.User import User
from booker.rest_interface.GymRestInterface import GymRestInterface
from exceptions.HttpRequestError import HttpRequestError
from booker.club.Club import Club
from datetime import datetime, timedelta
import json

class CityFitRestInterface(GymRestInterface):


    def __init__(self):
        super().__init__()
        self.request.base_url = 'https://klubowicz.cityfit.pl/api'
        self.request.add_header('Content-Type','application/json')
    
    def login(self, user: User):
        data = {
            "email": user.get_email(),
            "password": user.get_password()
        }  

        uri = '/tokens' 
        response = self.request.login(uri, data=data)

        if response.status_code != 200:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)
        
        response_json = json.loads(response.text)
        self.request.add_header ('Authorization','Bearer ' + response_json['accessToken'])


    def get_weekly_classes(self, club: Club) -> str:

        date_from = datetime.now().strftime("%Y-%m-%d")
        date_to = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        uri = f'/classes/schedule?dateFrom={date_from}&dateTo={date_to}&clubId={club.get_id()}&clubSchedule=true'
        response = self.request.get(uri)
        if response.status_code != 200:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)

        return response.text

 
    def book_class(self,activity: Activity):
        data = {
            "reservationDate": activity.date
        }
        uri = '/me/reservations/'+str(activity.id)
        
        response = self.request.post_json(uri, data)

        if response.status_code != 201:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)

    def cancel_booking(self,activity: Activity):
        #TODO niezaimplementowane
        pass


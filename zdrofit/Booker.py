from rest.BaseRequest import BaseRequest

from app_config.AppConfig import AppConfig
from exceptions.HttpRequestError import HttpRequestError
from time import sleep
from app_logger.AppLogger import AppLogger
from zdrofit.ActivityList import ActivityList

#TODO - Zaimplementować wylogowywanie się
#TODO - Dokumentację w stylu pytonowym w kodzie zrobić i spróbować wygerować
#TODO - jakiś refaktoring, wyodrębnić kilka klas, bo zdaje się, że już za dużo dopowiedzialności w jednej. mo
#       może jakiś iterface, który byłby wywoływany zamiast metody w klasie Scrapper?
#TODO - cancel booking - nie działa
#TODO - testy automatyczne?
#TODO - jakiś mail, info cokolwiek, jak po X probach nie uda się zaklepać
#TODO - adresy usług do ini przenieść
#TODO - wywołanie skryptów - zrobić jeden a parametry przekazywać podczas wywołania z lini poleceń w crontab
#TODO - po zabukowaniu sprawdzać, czy activity występuje w kalendarzu 

class Booker:

    config = None
    logger = None
    email = None
    request: BaseRequest

    clubs = {
        'gdansk-przymorze': 33,
        'gdansk-manhattan': 32,
        'gdynia-chwarzno': 43
    }

    def __init__(self, account: str, app_config: AppConfig, logger: AppLogger):
        self.logger = logger
        self.app_config = app_config
        self.user_name = self.app_config.get_account_param(account,'email')
        self.password =  self.app_config.get_account_param(account,'password')
        self.request = BaseRequest()

    def __login(self):
        data = {
            "RememberMe": "false",
            "Login": self.user_name,
            "Password": self.password
        }  

        uri = '/ClientPortal2/Auth/Login' 
        response = self.request.login(uri, data=data)

        if response.status_code != 200:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)

        self.logger.info(f'{self.user_name} has successfully logged in')

    def get_weekly_classes(self, club_id) -> ActivityList:
        data = {
            "clubId": club_id,
            "categoryId": 'null',
            "daysInWeek": '7'
        }
        uri = '/ClientPortal2/Classes/ClassCalendar/WeeklyClasses'
        response = self.request.post(uri, data=data)
        if response.status_code != 200:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)
 
        return ActivityList(response.text)

 
    def get_activities(self, club_name, activities=None, weekday=None, hour=None ,bookable_only=False):
        
        try:
            self.__login()
            club_id = self.clubs[club_name]
            activity_list = self.get_weekly_classes(club_id)
            if activities != None:
                activity_list.filter_by_activity(activities)
            if bookable_only:
                activity_list.filter_by_status('Bookable')
            if weekday != None:
                activity_list.filter_by_weekday(weekday)
            if hour != None:
                activity_list.filter_by_hour(hour)

            activity_list.sort()
            activity_list.print()
        
        except HttpRequestError as e:
            self.logger.error(e.message)
             
    def book_activity(self, club_name, activity_name, weekday, hour, retry_nr=50, seconds_between_retry=5):
        
        self.logger.info(f"Trying to book {activity_name} at club: {club_name}, weekday: {weekday}  hour: {hour}")
        
        try:
            self.__login()
            club_id = self.clubs[club_name]
            activity_list = self.get_weekly_classes(club_id)
        except HttpRequestError as e:
            self.logger.error(e.message)
            return
        except Exception as e:
            self.logger.error(e)
            return            

        activity_list.filter_by_activity(activity_name)
        activity_list.filter_by_weekday(weekday)
        activity_list.filter_by_hour(hour)
        activity_list.sort()

        if activity_list.get_activity_count() == 0:
            self.logger.info(f"Requested activity not found in callendar")
            return
        
        activity = activity_list.get_first_activity()
        self.logger.info(activity.get_log_found_message())
        request_nr = 1
        while request_nr <= retry_nr:
            
            try:
                self.__book_class(activity.id)
                self.logger.info(f"Activity {activity_name} booked successfully")
                break
            except HttpRequestError as e:
                if request_nr < retry_nr:
                    retry_message = f", retry in {seconds_between_retry} seconds ..."
                else:
                    retry_message = f", maximum nr of attempts excedeed, quiting ..."
                
                self.logger.info(f"Activity {activity_name} is not availiable for booking, attempt {request_nr}/{retry_nr}{retry_message}, {e.message}")
                request_nr = request_nr + 1
                sleep(seconds_between_retry)

    def cancel_booking(self, club_name, activity_name, weekday, hour):
        
        self.logger.info(f"Trying to cancel booking {activity_name} at club: {club_name}, weekday: {weekday}  hour: {hour}")
        
        try:
            self.__login()
            club_id = self.clubs[club_name]
            activity_list = self.get_weekly_classes(club_id)
        except HttpRequestError as e:
            self.logger.error(e.message)
            return
        except Exception as e:
            self.logger.error(e)
            return            

        activity_list.filter_by_activity((activity_name))
        activity_list.filter_by_weekday((weekday))
        activity_list.filter_by_hour((hour))
        activity_list.filter_by_status('Booked')
 
        if activity_list.get_activity_count() == 0:
            self.logger.info(f"Activity is not availiable for cancelling")
            return
        
        activity = activity_list.get_first_activity()
        self.logger.info(activity.get_log_found_message())

        try:
            self.__cancel_booking(activity.id)
        except HttpRequestError as e:
            self.logger.error(e.message)
            return
        except Exception as e:
            self.logger.error(e)
            return   
        
        self.logger.info(f"Activity {activity_name} booking cancelled successfully")


    def __book_class(self,class_id):
        data = {
            "classId": class_id
        }
        uri = '/ClientPortal2/Classes/ClassCalendar/BookClass'
        
        response = self.request.post(uri, data=data)

        if response.status_code != 200:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)

    def __cancel_booking(self,class_id):
        data = {
            "classId": class_id
        }
        uri = '/ClientPortal2/Classes/ClassCalendar/CancelBooking'
        
        response = self.request.post(uri, data=data)
        if response.status_code != 200:
            raise HttpRequestError(uri, response.status_code, response.reason, response.content)

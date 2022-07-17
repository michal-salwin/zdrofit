from blueemail.EmailActivityNotFound import EmailActivityNotFound
from blueemail.EmailMaxRetryExceeded import EmailMaxRetryExceeded
from blueemail.EmailSender import EmailSender
from blueemail.EmailSuccess import EmailSuccess
from booker.activity_list.ActivityList import ActivityList


from booker.rest_interface.GymRestInterface import GymRestInterface
from exceptions.HttpRequestError import HttpRequestError
from time import sleep
from app_logger.AppLogger import AppLogger
from booker.Activity import Activity
from booker.ActivityList import ActivityList
from booker.club.ZdrofitClub import Club
from booker.User import User

class Booker:

    config = None
    logger = None
    user = None
    email_sender: EmailSender
    rest_interface: GymRestInterface
    list_builder: ActivityList

    def __init__(self, user: User, rest_interface: GymRestInterface, list_builder: ActivityList):
        self.user = user
        self.rest_interface = rest_interface
        self.list_builder = list_builder
        self.email_sender = EmailSender()
        self.logger = AppLogger()

    def __login(self):
        self.rest_interface.login(self.user)
        self.logger.info(f'{self.user.get_email()} has successfully logged in')

    def get_weekly_classes(self, club: Club) -> ActivityList:
        classes_json = self.rest_interface.get_weekly_classes(club)
        return ActivityList(self.list_builder.build_activity_list(classes_json, club))

    def get_activities(self, club: Club, activities=None, weekday=None, hour=None ,bookable_only=False):
        
        try:
            self.__login()
            activity_list = self.get_weekly_classes(club)
            print(activity_list)
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
             
    def __book_class(self,class_id):
        self.rest_interface.book_class(class_id)

    def __cancel_booking(self,class_id):
        self.rest_interface.cancel_booking(class_id)


    def book_activity(self, activity: Activity, nr_of_retries=50, seconds_between_retry=5):
        
        self.logger.info(f"Trying to book {activity.name} at club: {activity.club.get_name()}, weekday: {activity.weekday}  hour: {activity.hour}")
        
        try:
            self.__login()
            activity_list = self.get_weekly_classes(activity.club)
        except HttpRequestError as e:
            self.logger.error(e.message)
            return
        except Exception as e:
            self.logger.error(e)
            return

        activity_list.filter_by_activity(activity.name)
        activity_list.filter_by_weekday(activity.weekday)
        activity_list.filter_by_hour(activity.hour)
        activity_list.sort()

        if activity_list.get_activity_count() == 0:
            self.logger.info(f"Requested activity not found in callendar")
            self.email_sender.send(EmailActivityNotFound(self.user,activity).get_message())
            return
        
        activity = activity_list.get_first_activity()
        self.logger.info(activity.get_log_found_message())
        request_nr = 1
        while request_nr <= nr_of_retries:
            
            try:
                self.__book_class(activity.id)
                self.email_sender.send(EmailSuccess(self.user,activity).get_message())
                self.logger.info(f"Activity {activity.name} booked successfully")
                return
            except HttpRequestError as e:
                if request_nr < nr_of_retries:
                    retry_message = f", retry in {seconds_between_retry} seconds ..."
                else:
                    retry_message = f", maximum nr of attempts exceeded, quiting ..."
                
                self.logger.info(f"Activity {activity.name} is not availiable for booking, attempt {request_nr}/{nr_of_retries}{retry_message}, {e.message}")
                request_nr = request_nr + 1
                sleep(seconds_between_retry)
        
        self.email_sender.send(EmailMaxRetryExceeded(self.user,activity).get_message())

    def cancel_booking(self, activity: Activity, weekday, hour):
        
        self.logger.info(f"Trying to cancel booking {activity.name} at club: {activity.club.get_name()}, weekday: {weekday}  hour: {hour}")
        
        try:
            self.__login()
            activity_list = self.get_weekly_classes(activity.club)
        except HttpRequestError as e:
            self.logger.error(e.message)
            return
        except Exception as e:
            self.logger.error(e)
            return

        activity_list.filter_by_activity((activity.name))
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
        
        self.logger.info(f"Activity {activity.name} booking cancelled successfully")



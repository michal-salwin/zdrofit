from blueemail.EmailActivityNotFound import EmailActivityNotFound
from blueemail.EmailMaxRetryExceeded import EmailMaxRetryExceeded
from blueemail.EmailSender import EmailSender
from blueemail.EmailSuccess import EmailSuccess
from booker.activity_list.ActivityListBuilder import ActivityListBuilder


from booker.rest_interface.GymRestInterface import GymRestInterface
from exceptions.HttpRequestError import HttpRequestError
from time import sleep
from app_logger.AppLogger import AppLogger
from booker.Activity import Activity
from booker.ActivityList import ActivityList
from booker.club.Club import Club
from booker.User import User

class Booker:

    config = None
    logger = None
    user = None
    email_sender: EmailSender
    rest_interface: GymRestInterface
    list_builder: ActivityListBuilder

    def __init__(self, user: User, rest_interface: GymRestInterface, list_builder: ActivityListBuilder):
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
             
    def __book_class(self,activity: Activity):
        self.rest_interface.book_class(activity)

    def __cancel_booking(self,activity: Activity):
        self.rest_interface.cancel_booking(activity)


    def book_activity(self, activity_to_book: Activity, nr_of_retries=50, seconds_between_retry=5):
        
        self.logger.info(f"Trying to book {activity_to_book.name} at club: {activity_to_book.club.get_name()}, weekday: {activity_to_book.weekday}  hour: {activity_to_book.hour}")
        
        try:
            self.__login()
            activity_list = self.get_weekly_classes(activity_to_book.club)
        except HttpRequestError as e:
            self.logger.error(e.message)
            return
        except Exception as e:
            self.logger.error(e)
            return

        activity_list.filter_by_activity(activity_to_book.name)
        activity_list.filter_by_weekday(activity_to_book.weekday)
        activity_list.filter_by_hour(activity_to_book.hour)
        activity_list.sort()

        if activity_list.get_activity_count() == 0:
            self.logger.info(f"Requested activity not found in callendar, trying to book another at the same time")
            activity_list = self.get_weekly_classes(activity_to_book.club)
            activity_list.filter_by_weekday(activity_to_book.weekday)
            activity_list.filter_by_hour(activity_to_book.hour)
            activity_list.sort()

        if activity_list.get_activity_count() == 0:
            self.logger.info(f"Requested activity not found in callendar")
            self.email_sender.send(EmailActivityNotFound(self.user,activity_to_book, None).get_message())
            return

        activity_booked = activity_list.get_first_activity()
        self.logger.info(activity_booked.get_log_found_message())
        request_nr = 1
        while request_nr <= nr_of_retries:
            
            try:
                self.__book_class(activity_booked)
                self.email_sender.send(EmailSuccess(self.user, activity_to_book, activity_booked).get_message())
                self.logger.info(f"Activity {activity_booked.name} booked successfully")
                return
            except HttpRequestError as e:
                if request_nr < nr_of_retries:
                    retry_message = f", retry in {seconds_between_retry} seconds ..."
                else:
                    retry_message = f", maximum nr of attempts exceeded, quiting ..."
                
                self.logger.info(f"Activity {activity_booked.name} is not availiable for booking, attempt {request_nr}/{nr_of_retries}{retry_message}, {e.message}")
                request_nr = request_nr + 1
                sleep(seconds_between_retry)
        
        self.email_sender.send(EmailMaxRetryExceeded(self.user,activity_to_book, activity_booked).get_message())

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
            self.__cancel_booking(activity)
        except HttpRequestError as e:
            self.logger.error(e.message)
            return
        except Exception as e:
            self.logger.error(e)
            return   
        
        self.logger.info(f"Activity {activity.name} booking cancelled successfully")




import requests
import json
from exceptions.HttpRequestError import HttpRequestError
from log.Logger import Logger
from time import sleep
from datetime import date
import configparser


#TODO - Zaimplementować wylogowywanie się
#TODO - Dokumentację w stylu pytonowym w kodzie zrobić i spróbować wygerować
#TODO - jakiś refaktoring, wyodrębnić kilka klas, bo zdaje się, że już za dużo dopowiedzialności w jednej. mo
#       może kjakiś iterface, który byłby wywoływany zamiast metody w klasei zdrofitscrapper?
#TODO - przerobić tak, aby posługiwać się nazwami klubów a nie odentyfikatorami
#TODO - cancel booking - nie działa
#TODO - activity_Table_heeaders na enuma zamienić
#TODO - testy automatyczne?
#TODO - jakiś mail, info cokolwiek, jak po X probach nie uda się zaklepać

class ZdrofitScrapper:

    __conf = None

    @staticmethod
    def config():
        if ZdrofitScrapper.__conf is None: 
            ZdrofitScrapper.__conf = configparser.ConfigParser()
            ZdrofitScrapper.__conf.read('scrapper.ini')
        return ZdrofitScrapper.__conf

    def __init__(self, account):
        self.base_url = 'https://zdrofit.perfectgym.pl/'
        self.activity_table = []
        self.logger = Logger()
        self.activity_table_headers = {'id': 0, 'status': 1, 'status_reason': 2, 'name': 3, 'trainer': 4, 'weekday': 5, 'date': 6, 'hour': 7}
        self.user_name = ZdrofitScrapper.config().get(section=f'zdrofit.account.{account}',option='email')
        self.password =  ZdrofitScrapper.config().get(section=f'zdrofit.account.{account}',option='password')


    def __login(self):
        data = {
            "RememberMe": "false",
            "Login": self.user_name,
            "Password": self.password
        }   
        url = self.base_url+'/ClientPortal2/Auth/Login' 
        response = requests.post(url, data=data)
        if response.status_code != 200:
            raise HttpRequestError(url, response.status_code, response.content)

        self.cookies = response.cookies
        self.logger.info(f'{self.user_name} has successfully logged in')

    def __get_available_classes(self):
        response = requests.get(self.base_url+'ClientPortal2/Clubs/GetAvailableClassesClubs/', cookies=self.cookies)
 
    def __get_weekly_classes(self, club_id):
        data = {
            "clubId": club_id,
            "categoryId": 'null',
            "daysInWeek": '7'
        }
        url = self.base_url+'/ClientPortal2/Classes/ClassCalendar/WeeklyClasses'
        response = requests.post(url, data=data, cookies=self.cookies)
        if response.status_code != 200:
            raise HttpRequestError(url, response.status_code, response.content)
 
        self.activity_table = []
        json_data = json.loads(response.text)

        for zone in json_data['CalendarData']:
            for hours in zone['ClassesPerHour']:
                for days in hours['ClassesPerDay']:
                    item = []
                    for activity in days:
                        self.activity_table.append([
                            activity['Id'],
                            activity['Status'],
                            str(activity['StatusReason']),
                            activity['Name'],
                            activity['Trainer'],
                            date.fromisoformat(str(activity['StartTime'][:10])).strftime('%A'),
                            activity['StartTime'][:10],
                            activity['StartTime'][11:16]
                        ])                        
 
    def __sort_activity_table(self):
        #sort by date, time
        self.activity_table = sorted(self.activity_table,key=lambda x:(x[self.activity_table_headers['date']], x[self.activity_table_headers['hour']]))
    
    def __print_activity_table(self):
        for item in list(self.activity_table):
            print ("{:<7} {:<15} {:<20} {:<30} {:<30} {:<13} {:<13} {:<13}".format(*item))
        if len(self.activity_table) == 0:
            print ("Activity list is empty.")

    def __filter_activity_table_by_activity(self, activity_list):
        self.activity_table = [x for x in self.activity_table if x[self.activity_table_headers['name']] in activity_list]

    def __filter_activity_table_by_status(self,status):
        self.activity_table = [x for x in self.activity_table if x[self.activity_table_headers['status']] == status]

    def __filter_activity_table_by_weekday(self,weekday):
        self.activity_table = [x for x in self.activity_table if x[self.activity_table_headers['weekday']] == weekday]

    def __filter_activity_table_by_hour(self,hour):
        self.activity_table = [x for x in self.activity_table if x[self.activity_table_headers['hour']] == hour]


    def __write_file(self,file_name,content):
        f = open(file_name, "w")
        f.write(content)
        f.close()     

    def get_activities(self, club_id,activity_list=None, weekday=None, hour=None ,bookable_only=False):
        
        try:
            self.__login()
            self.__get_weekly_classes(club_id)
            if activity_list != None:
                self.__filter_activity_table_by_activity(activity_list)
            if bookable_only:
                self.__filter_activity_table_by_status('Bookable')
            if weekday != None:
                self.__filter_activity_table_by_weekday(weekday)
            if hour != None:
                self.__filter_activity_table_by_hour(hour)

            self.__sort_activity_table()
            self.__print_activity_table()
        except HttpRequestError as e:
            self.logger.error(e.message)
        #except Exception as e:
         #   self.logger.error(e)
             
    def book_activity(self, club_id, activity_name, weekday, hour, retry_nr=50, seconds_between_retry=5):
        
        self.logger.info(f"Trying to book {activity_name} at club_id: {club_id}, weekday: {weekday}  hour: {hour}")
        
        try:
            self.__login()
            self.__get_weekly_classes(club_id)
        except HttpRequestError as e:
            self.logger.error(e.message)
            return
        except Exception as e:
            self.logger.error(e)
            return            

        self.__filter_activity_table_by_activity((activity_name))
        self.__filter_activity_table_by_weekday((weekday))
        self.__filter_activity_table_by_hour((hour))
        self.__sort_activity_table()

        if len(self.activity_table) == 0:
            self.logger.info(f"Requested activity not found in callendar")
            return
        
        #TODO wypisywanie aktywności w logu zamienić na funkcję
        self.logger.info(
                f"Found Activity {activity_name}, "
                f"status: {self.activity_table[0][self.activity_table_headers['status']]}({self.activity_table[0][self.activity_table_headers['status_reason']]}), "
                f"starting at {self.activity_table[0][self.activity_table_headers['date']]} {self.activity_table[0][self.activity_table_headers['hour']]}")

        request_nr = 1
        while request_nr <= retry_nr:
            
            try:
                self.__book_class(self.activity_table[0][0])
                self.logger.info(f"Activity {activity_name} booked successfully")
                break
            except HttpRequestError as e:
                if request_nr < retry_nr:
                    retry_message = f", retry in {seconds_between_retry} seconds ..."
                else:
                    retry_message = f", maximum nr of attempts excedeed, quiting ..."
                
                self.logger.info(f"Activity {activity_name} is not availiable for booking, attempt {request_nr}/{retry_nr}{retry_message}")
                request_nr = request_nr + 1
                sleep(seconds_between_retry)

    def cancel_booking(self, club_id, activity_name):
        
        try:
            self.__login()
            self.__get_weekly_classes(club_id)
            self.__filter_activity_table_by_activity((activity_name))
            self.__filter_activity_table_by_status('Booked')
            if len(self.activity_table) == 0:
                self.logger.info(f"Activity {activity_name} is not availiable for cancelling")
            else:
                self.__cancel_booking(self.activity_table[0][0])
                self.logger.info(f"Activity {activity_name} booking cancelled successfully")
        except HttpRequestError as e:
            self.logger.error(e.message)


    def __book_class(self,class_id):
        data = {
            "classId": class_id
        }
        url = self.base_url+'/ClientPortal2/Classes/ClassCalendar/BookClass'    
        
        response = requests.post(url, data=data, cookies=self.cookies)

        if response.status_code != 200:
            raise HttpRequestError(url, response.status_code, response.content)

        self.cookies = response.cookies

    def __cancel_booking(self,class_id, retry=10):
        data = {
            "classId": class_id
        }
        url = self.base_url+'/ClientPortal2/Classes/ClassCalendar/CancelBooking'
        
        response = requests.post(url, data=data, cookies=self.cookies)
        if response.status_code != 200:
            raise HttpRequestError(url, response.status_code, response.content)

        self.cookies = response.cookies


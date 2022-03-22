import requests
import json
from exceptions.HttpRequestError import HttpRequestError
from log.Logger import Logger
from time import sleep

#TODO Zaimplementować wylogowywanie się

class ZdrofitScrapper:

    def __init__(self, user_name, password):
        self.base_url = 'https://zdrofit.perfectgym.pl/'
        self.activities_table = []
        self.logger = Logger()

        self.user_name = user_name
        self.password =  password

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
        #self.write_file('GetAvailableClassesClubs.json',json.dumps(json.loads(response.text), indent=2))

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
        #self.write_file('WeeklyClasses.json',json.dumps(json.loads(response.text), indent=2))

        self.activities_table = []
        json_data = json.loads(response.text)

        for zone in json_data['CalendarData']:
            for hours in zone['ClassesPerHour']:
                for days in hours['ClassesPerDay']:
                    for activity in days:
                        self.activities_table.append([
                            activity['Id'],
                            activity['Status'],
                            str(activity['StatusReason']),
                            activity['Name'],
                            activity['Trainer'],
                            activity['StartTime'][:10],
                            activity['StartTime'][11:]
                        ])
 
    def __sort_activity_table(self):
        #sort by date, time
        self.activities_table = sorted(self.activities_table,key=lambda x:(x[5], x[6]))
    
    def __print_activity_table(self):
        for item in list(self.activities_table):
            print ("{:<7} {:<15} {:<20} {:<30} {:<30} {:<13} {:<13}".format(*item))
        if len(self.activities_table) == 0:
            print ("Activity list is empty.")

    def __filter_activity_table_by_activity(self, activity_list):
        self.activities_table = [x for x in self.activities_table if x[3] in activity_list]

    def __filter_activity_table_by_status(self,status):
        self.activities_table = [x for x in self.activities_table if x[1] == status]

    def __write_file(self,file_name,content):
        f = open(file_name, "w")
        f.write(content)
        f.close()     

    def get_activities(self, club_id,activity_list=None, bookable_only=False):
        
        try:
            self.__login()
            self.__get_weekly_classes(club_id)
            if activity_list != None:
                self.__filter_activity_table_by_activity(activity_list)
            if bookable_only:
                self.__filter_activity_table_by_status('Bookable')
            self.__sort_activity_table()
            self.__print_activity_table()
        except HttpRequestError as e:
            self.logger.error(e.message)
        except Exception as e:
            self.logger.error(e)
             
    def book_activity(self, club_id, activity_name, retry_nr=10, seconds_between_retry=5):
        
        self.logger.info(f"Trying to book {activity_name} at club_id: {club_id}")
        
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
        self.__sort_activity_table()

        if len(self.activities_table) == 0:
            self.logger.info(f"Activity {activity_name} not found in callendar")
            return
        
        #TODO wypisywanie aktywności w logu zamienić na funkcję
        self.logger.info(f"Found Activity {activity_name}, status: {self.activities_table[0][1]}({self.activities_table[0][2]}), starting at {self.activities_table[0][5]} {self.activities_table[0][6]}")

        request_nr = 1
        while request_nr <= retry_nr:
            
            try:
                self.__book_class(self.activities_table[0][0])
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
            if len(self.activities_table) == 0:
                self.logger.info(f"Activity {activity_name} is not availiable for cancelling")
            else:
                self.__cancel_booking(self.activities_table[0][0])
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


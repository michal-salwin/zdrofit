from zdrofit.Activity import Activity
import json
from datetime import date

class ActivityList:

    activity_list: list[Activity] = []

    def __init__(self,activity_list_json: str):
        self.build_activity_list(activity_list_json)

    def build_activity_list(self,activity_list_json):

        json_data = json.loads(activity_list_json)

        for zone in json_data['CalendarData']:
            for hours in zone['ClassesPerHour']:
                for days in hours['ClassesPerDay']:
                    for activity in days:
                        a = Activity()
                        a.id = activity['Id']
                        a.status = activity['Status']
                        a.status_reason = activity['StatusReason']
                        a.name = activity['Name']
                        a.trainer = activity['Trainer']
                        a.weekday = date.fromisoformat(str(activity['StartTime'][:10])).strftime('%A')
                        a.date = activity['StartTime'][:10]
                        a.hour = activity['StartTime'][11:16]

                        self.activity_list.append(a)
 
    def sort(self):
        #sort by date, time
        self.activity_list = sorted(self.activity_list,key=lambda x:(x.date, x.hour))
    
    def print(self):
        for item in list(self.activity_list):
            #item.print_line()
            print(item)
        if len(self.activity_list) == 0:
            print ("Activity list is empty.")

    def filter_by_activity(self, activities):
        self.activity_list = [x for x in self.activity_list if x.name in activities]

    def filter_by_status(self,status):
        self.activity_list = [x for x in self.activity_list if x.status == status]

    def filter_by_weekday(self,weekday):
        self.activity_list = [x for x in self.activity_list if x.weekday == weekday]

    def filter_by_hour(self,hour):
        self.activity_list = [x for x in self.activity_list if x.hour == hour]

    def get_first_activity(self):
        return self.activity_list[0]

    def get_activity_count(self) -> int:
        return len (self.activity_list)

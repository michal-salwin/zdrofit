from booker.Activity import Activity

class ActivityList:

    activity_list: list[Activity] = []

    def __init__(self,activity_list: list[Activity]):
        self.activity_list = activity_list

    def sort(self):
        #sort by date, time
        self.activity_list = sorted(self.activity_list,key=lambda x:(x.date, x.hour))
    
    def print(self):
        for item in list(self.activity_list):
            print(item)
        if len(self.activity_list) == 0:
            print ("Activity list is empty.")

    def filter_by_activity(self, activities):
        if activities:
            self.activity_list = [x for x in self.activity_list if x.name in activities]

    def filter_by_status(self,status):
        self.activity_list = [x for x in self.activity_list if x.status == status]

    def filter_by_weekday(self,weekday):
        self.activity_list = [x for x in self.activity_list if x.weekday == weekday]

    def filter_by_hour(self,hour):
        self.activity_list = [x for x in self.activity_list if x.hour == hour]

    def filter_by_id(self,id):
        self.activity_list = [x for x in self.activity_list if x.id == id]

    def get_first_activity(self):
        return self.activity_list[0]

    def get_activity_count(self) -> int:
        return len (self.activity_list)

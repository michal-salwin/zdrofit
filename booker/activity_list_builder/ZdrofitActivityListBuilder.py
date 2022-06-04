
from booker.Activity import Activity
from booker.Club import Club
from booker.activity_list_builder.ActivityListBuilder import ActivityListBuilder
import json
from datetime import date

class ZdrofitActivityListBuilder(ActivityListBuilder):

    def build_activity_list(self, json_activity_list: str, club: Club) -> list[Activity]:

        activity_list: list[Activity] = []

        json_data = json.loads(json_activity_list)

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
                        a.limit = activity['BookingIndicator']['Limit']
                        a.available = activity['BookingIndicator']['Available']
                        a.club = club
                        activity_list.append(a)
        
        return activity_list    
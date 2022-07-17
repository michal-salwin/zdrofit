
from booker.Activity import Activity
from booker.club.ZdrofitClub import Club
from booker.activity_list.ActivityList import ActivityList
import json
from datetime import date

class CityFitActivityList(ActivityList):

    def build_activity_list(self, json_activity_list: str, club: Club) -> list[Activity]:

        activity_list: list[Activity] = []

        json_data = json.loads(json_activity_list)

        for activity in json_data:
            a = Activity()
            a.id = activity['id']
            a.status = "Bookable"
            a.status_reason = ""
            a.name = activity['name'].strip()
            a.trainer = activity['instructor']['name'][:20]
            a.weekday = date.fromisoformat(str(activity['startDate'][:10])).strftime('%A')
            a.date = activity['startDate'][:10]
            a.hour = activity['startDate'][11:16]
            a.limit = activity['maximumParticipants']
            a.available = activity['maximumParticipants'] - activity['participants']['participantsOk']
            a.club = club
            activity_list.append(a)
        
        return activity_list    
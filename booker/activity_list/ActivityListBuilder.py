from abc import ABC, abstractmethod

from booker.Activity import Activity
from booker.club.Club import Club

class ActivityListBuilder(ABC):

    @abstractmethod
    def build_activity_list(self, json_data: str, club: Club) -> list[Activity]:
        pass
from abc import ABC, abstractmethod

from booker.Activity import Activity
from booker.Club import Club

class ActivityListBuilder(ABC):

    @abstractmethod
    def build_activity_list(self, json_data: str) -> list[Activity]:
        pass
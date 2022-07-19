from datetime import datetime


class BookingStatsCollector:
    __nr_of_tries: int
    __tries_limit: int
    __seconds_between_tries: int
    __start_time: datetime
    __stop_time: datetime

    def __init__(self, tries_limit: int, seconds_between_tries: int) -> None:
        self.__nr_of_tries = 0
        self.__start_time = datetime.now()
        self.__tries_limit = tries_limit
        self.__seconds_between_tries = seconds_between_tries

    def add_try(self)-> None:
        self.__nr_of_tries += 1
        self.__stop_time = datetime.now()
    
    def get_nr_of_tries(self) -> int:
        return self.__nr_of_tries

    def get_tries_limit(self) -> int:
        return self.__tries_limit

    def get_seconds_between_tries(self) -> int:
        return self.__seconds_between_tries

    def get_start_time(self) -> datetime:
        return self.__start_time

    def get_stop_time(self) -> datetime:
        return self.__stop_time

from datetime import datetime


class Activity:
    id:             int = None
    status:         str = None
    status_reason:  str = None
    name:           str = None
    trainer:        str = None
    weekday:        str = None
    date:           datetime = None
    hour:           str = None
    limit:          int = None
    available:      int = None
    club_name:      str = None

    def __init__(self):
        pass

    def xstr(self, s):
        if s is None:
            return ''
        return str(s)

    def __str__(self):
         return str('{:<7} {:<15} {:<20} {:<30} {:<23} {:<13} {:<13} {:<5} {:>7}'.
            format(self.id, 
                   self.status, 
                   self.xstr(self.status_reason), 
                   self.name,
                   self.trainer, 
                   self.weekday, 
                   self.date, 
                   self.hour,
                   str(f'{self.available}/{self.limit}')
            )
    )

    def get_log_found_message(self) -> str:
        return f"Found Activity {self.name}, status: {self.status} starting at {self.weekday}, {self.date} {self.hour}, availability: {self.available}/{self.limit}"

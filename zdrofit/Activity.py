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

    def __init__(self):
        pass

    def __str__(self):
         return str('{:<7} {:<15} {:<20} {:<30} {:<30} {:<13} {:<13} {:<13}'.
            format(self.id, 
                   self.status, 
                   str(self.status_reason), 
                   self.name,
                   self.trainer, 
                   self.weekday, 
                   self.date, 
                   self.hour
            )
    )

    def get_log_found_message(self) -> str:
        return f"Found Activity {self.name}, status: {self.status} starting at {self.weekday}, {self.date} {self.hour}"

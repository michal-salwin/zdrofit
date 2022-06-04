from datetime import date
from app_config.AppConfig import AppConfig
from blueemail.EmailSender import EmailSender

from blueemail.EmailSuccess import EmailSuccess
from booker.Activity import Activity
from booker.Club import Club
from booker.User import User

config = AppConfig()
user = User('MS',config)

sender = EmailSender()

activity = Activity()
activity.id = 123456
activity.available = 19
activity.limit = 20
activity.name = "Testowe ćwiczenia"
activity.date = date.today() 
activity.hour = "18:30"
activity.status = 'Booked'
activity.weekday = 'Sunday'
activity.club = Club('gdansk-przymorze')

sender.send(EmailSuccess(user,activity).get_message())





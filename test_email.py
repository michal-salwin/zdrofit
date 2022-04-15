from datetime import date
from app_config.AppConfig import AppConfig
from blueemail.ZdrofitEmailSender import ZdrofitEmailSender

from blueemail.ZdrofitEmailSuccess import ZdrofitEmailSuccess
from zdrofit.Activity import Activity
from zdrofit.Club import Club
from zdrofit.User import User

config = AppConfig()
user = User('MS',config)

sender = ZdrofitEmailSender()

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

sender.send(ZdrofitEmailSuccess(user,activity).get_message())
#mail.send_on_activity_not_found(activity)
#mail.send_on_max_retry_exceeded(activity,50)





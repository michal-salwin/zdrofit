from datetime import date
from app_config.AppConfig import AppConfig

from blueemail.ZdrofitEmail import ZdrofitEmail
from zdrofit.Activity import Activity
from zdrofit.Club import Club
from zdrofit.User import User

config = AppConfig()
user = User('MS',config)
mail = ZdrofitEmail(user)

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

mail.send_on_successful_booking(activity)
mail.send_on_activity_not_found(activity)
mail.send_on_max_retry_exceeded(activity,50)





from datetime import date
from blueemail.ZdrofitEmail import ZdrofitEmail
from zdrofit.Activity import Activity

mail = ZdrofitEmail('MS')
activity = Activity()
activity.id = 123456
activity.available = 19
activity.limit = 20
activity.name = "Testowe ćwiczenia"
activity.date = date.today()
activity.hour = "18:30"
activity.status = 'Booked'
activity.weekday = 'Sunday'

mail.send_on_successful_booking(activity)


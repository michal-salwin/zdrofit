from datetime import date
from app_config.AppConfig import AppConfig
from blueemail.EmailActivityNotFound import EmailActivityNotFound
from blueemail.EmailMaxRetryExceeded import EmailMaxRetryExceeded
from blueemail.EmailSender import EmailSender

from blueemail.EmailSuccess import EmailSuccess
from booker.Activity import Activity
from booker.BookingStatsCollector import BookingStatsCollector
from booker.club.ClubFactory import Club, ClubFactory
from booker.User import User

config = AppConfig()
user = User('MS',config)

sender = EmailSender()

activity_to_book = Activity()
activity_to_book.name = "Testowe s ćwiczenia"
activity_to_book.date = date.today() 
activity_to_book.hour = "18:30"
activity_to_book.weekday = 'Sunday'
activity_to_book.club = ClubFactory('zdrofit','gdansk-przymorze').get_club()

activity_booked = Activity()
activity_booked.id = 123456
activity_booked.available = 19
activity_booked.limit = 20
activity_booked.name = "Testowe ćwiczenia"
activity_booked.date = date.today() 
activity_booked.hour = "18:30"
activity_booked.status = 'Booked'
activity_booked.weekday = 'Sunday'
activity_booked.club = ClubFactory('zdrofit','gdansk-przymorze').get_club()

stats = BookingStatsCollector(50,5)
stats.add_try()
stats.add_try()
stats.add_try()

sender.send(EmailSuccess(user,activity_to_book, activity_booked,stats).get_message())
sender.send(EmailActivityNotFound(user,activity_to_book).get_message())
sender.send(EmailMaxRetryExceeded(user,activity_to_book,stats,).get_message())





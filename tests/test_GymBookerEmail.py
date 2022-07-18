from datetime import date
import unittest
from app_config.AppConfig import AppConfig
from blueemail.EmailActivityNotFound import EmailActivityNotFound
from blueemail.EmailMaxRetryExceeded import EmailMaxRetryExceeded
from blueemail.EmailSuccess import EmailSuccess
from tests.TestCaseBase import TestCaseBase
from booker.Activity import Activity
from booker.club.ClubFactory import ClubFactory
from booker.User import User


class TestGymBookerEmail(TestCaseBase):

    def test_GymBookerEmailSuccess(self):

        config = AppConfig()
        user = User('MS', config)
        activity = self.prepare_activity()
        activity_booked = self.prepare_activity_booked()
        message = EmailSuccess(user, activity, activity_booked).get_message()
        self.assertEqual(user.get_email(),message.to_email)
        self.assertEqual(user.get_fullname(),message.to_name)
        self.assertEqual(message.subject,'GymBooker - automatyczna rejestracja')
        self.assertEqual(config.get(section='sendinblue', option='from_email'),message.from_email)
        self.assertEqual(config.get(section='sendinblue', option='from_name'),message.from_name)

    def test_GymBookerEmailActivityNotFound(self):

        config = AppConfig()
        user = User('MS', config)
        activity = self.prepare_activity()
        activity_booked = self.prepare_activity_booked()
        message = EmailActivityNotFound(user, activity, activity_booked).get_message()
        self.assertEqual(user.get_email(),message.to_email)
        self.assertEqual(user.get_fullname(),message.to_name)
        self.assertEqual(message.subject,'GymBooker - automatyczna rejestracja - błąd rejestracji')
        self.assertEqual(config.get(section='sendinblue', option='from_email'),message.from_email)
        self.assertEqual(config.get(section='sendinblue', option='from_name'),message.from_name)

    def test_GymBookerEmailMaxRetryExceeded(self):

        config = AppConfig()
        user = User('MS', config)
        activity = self.prepare_activity()
        activity_booked = self.prepare_activity_booked()
        message = EmailMaxRetryExceeded(user, activity, activity_booked).get_message()
        self.assertEqual(user.get_email(),message.to_email)
        self.assertEqual(user.get_fullname(),message.to_name)
        self.assertEqual(message.subject,'GymBooker - automatyczna rejestracja - błąd')
        self.assertEqual(config.get(section='sendinblue', option='from_email'),message.from_email)
        self.assertEqual(config.get(section='sendinblue', option='from_name'),message.from_name)


    def prepare_activity(self) -> Activity:
        activity = Activity()
        activity.id = 123456
        activity.available = 19
        activity.limit = 20
        activity.name = "Testowe ćwiczenia"
        activity.date = date.today() 
        activity.hour = "18:30"
        activity.status = 'Booked'
        activity.weekday = 'Sunday'
        activity.club = ClubFactory('zdrofit','gdansk-przymorze').get_club()

        return activity

    def prepare_activity_booked(self) -> Activity:
        activity = Activity()
        activity.id = 123456
        activity.available = 19
        activity.limit = 20
        activity.name = "Testowe ćwiczenia"
        activity.date = date.today() 
        activity.hour = "18:30"
        activity.status = 'Booked'
        activity.weekday = 'Sunday'
        activity.club = ClubFactory('zdrofit','gdansk-przymorze').get_club()

        return activity
if __name__ == '__main__':
    unittest.main()
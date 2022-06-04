from datetime import date
import unittest
from app_config.AppConfig import AppConfig
from blueemail.EmailActivityNotFound import EmailActivityNotFound
from blueemail.EmailMaxRetryExceeded import EmailMaxRetryExceeded
from blueemail.EmailSuccess import EmailSuccess
from tests.TestCaseBase import TestCaseBase
from booker.Activity import Activity
from booker.Club import Club
from booker.User import User


class TestZdrofitEmail(TestCaseBase):

    def test_ZdrofitEmailSuccess(self):

        config = AppConfig()
        user = User('MS', config)
        activity = self.prepare_activity()
        message = EmailSuccess(user, activity).get_message()
        self.assertEqual(user.get_email(),message.to_email)
        self.assertEqual(user.get_fullname(),message.to_name)
        self.assertEqual(message.subject,'Zdrofit -automatyczna rejestracja')
        self.assertEqual(config.get(section='sendinblue', option='from_email'),message.from_email)
        self.assertEqual(config.get(section='sendinblue', option='from_name'),message.from_name)

    def test_ZdrofitEmailActivityNotFound(self):

        config = AppConfig()
        user = User('MS', config)
        activity = self.prepare_activity()
        message = EmailActivityNotFound(user, activity).get_message()
        self.assertEqual(user.get_email(),message.to_email)
        self.assertEqual(user.get_fullname(),message.to_name)
        self.assertEqual(message.subject,'Zdrofit -automatyczna rejestracja - błąd rejestracji')
        self.assertEqual(config.get(section='sendinblue', option='from_email'),message.from_email)
        self.assertEqual(config.get(section='sendinblue', option='from_name'),message.from_name)

    def test_ZdrofitEmailMaxRetryExceeded(self):

        config = AppConfig()
        user = User('MS', config)
        activity = self.prepare_activity()
        message = EmailMaxRetryExceeded(user, activity).get_message()
        self.assertEqual(user.get_email(),message.to_email)
        self.assertEqual(user.get_fullname(),message.to_name)
        self.assertEqual(message.subject,'Zdrofit -automatyczna rejestracja - błąd')
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
        activity.club = Club('gdansk-przymorze')

        return activity


if __name__ == '__main__':
    unittest.main()
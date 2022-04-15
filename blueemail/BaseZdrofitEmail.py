from blueemail.HtmlMessage import HtmlMessage
from app_config.AppConfig import AppConfig
from zdrofit.Activity import Activity
from zdrofit.User import User
from abc import ABC, abstractmethod

class BaseZdrofitEmail(ABC):

    message: HtmlMessage = None

    def __init__(self, user: User, activity: Activity):

        self.config = AppConfig()
        self.activity = activity
        self.user = user
        self.message = self.prepare_message()

    def prepare_message(self) -> HtmlMessage:
        message = HtmlMessage()
        message.from_email = self.config.get(section='sendinblue', option='from_email')
        message.from_name = self.config.get(section='sendinblue', option='from_name')
        message.to_email = self.user.get_email()
        message.to_name =  self.user.get_fullname()
        message.cc_email = self.config.get(section='sendinblue', option='cc_email')
        message.cc_name = self.config.get(section='sendinblue', option='cc_name')
        return message

    @abstractmethod
    def get_message(self) -> HtmlMessage:
        pass
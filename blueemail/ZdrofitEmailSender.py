from blueemail.BaseZdrofitEmail import BaseZdrofitEmail
from blueemail.BlueEmail import BlueEmail
from blueemail.HtmlMessage import HtmlMessage
from app_config.AppConfig import AppConfig
from app_logger.AppLogger import AppLogger
from exceptions.SendInBlueEmailException import SendInBlueEmailException
from zdrofit.Activity import Activity
from zdrofit.User import User


class ZdrofitEmailSender:

    message: HtmlMessage = None

    def __init__(self):

        self.config = AppConfig()
        self.logger = AppLogger()
        self.email = BlueEmail(self.config.get(section='sendinblue', option='api_key'))

    def send(self, message: BaseZdrofitEmail):
        try:
            self.email.send_html_email(message)
        except SendInBlueEmailException as e:
            self.logger.error(f'Error sending email: {str(message)}')
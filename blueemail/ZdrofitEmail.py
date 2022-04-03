from blueemail.BlueEmail import BlueEmail, HtmlMessage
from app_config.AppConfig import AppConfig
from app_logger.AppLogger import AppLogger
from utils.RandomFileLineReader import RandomFileLineReader

class ZdrofitEmail:

    def __init__(self, account: str):

        self.config = AppConfig()
        self.logger = AppLogger()
        self.email = BlueEmail(self.config.get(section='sendinblue', option='api_key'),self.logger)
        self.account = account

    def send(self, subject: str, message: str):
        message = HtmlMessage()
        message.from_email = self.config.get(section='sendinblue', option='from_email')
        message.from_name = self.config.get(section='sendinblue', option='from_name')
        message.to_email = self.config.get_account_param(self.account,'email')
        message.to_name =  self.config.get_account_param(self.account,'name')
        message.cc_email = self.config.get(section='sendinblue', option='cc_email')
        message.cc_name = self.config.get(section='sendinblue', option='cc_name')
        message.subject = subject
        text = f'<html><body><h3>Zdrofit automatyczna rejestracja</h3><p>{message}</p></body></html>'
        message.content_html = text
        self.email.send_html_email(message)

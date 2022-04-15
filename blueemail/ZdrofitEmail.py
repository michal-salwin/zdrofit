from blueemail.BlueEmail import BlueEmail
from blueemail.HtmlMessage import HtmlMessage
from app_config.AppConfig import AppConfig
from app_logger.AppLogger import AppLogger
from exceptions.SendInBlueEmailException import SendInBlueEmailException
from utils.Weekday import Weekday
from zdrofit.Activity import Activity
from zdrofit.User import User

class ZdrofitEmail:

    def __init__(self, user: User):

        self.config = AppConfig()
        self.logger = AppLogger()
        self.email = BlueEmail(self.config.get(section='sendinblue', option='api_key'))
        self.user = user

    def prepare_message(self) -> HtmlMessage:
        message = HtmlMessage()
        message.from_email = self.config.get(section='sendinblue', option='from_email')
        message.from_name = self.config.get(section='sendinblue', option='from_name')
        message.to_email = self.user.get_email()
        message.to_name =  self.user.get_fullname()
        message.cc_email = self.config.get(section='sendinblue', option='cc_email')
        message.cc_name = self.config.get(section='sendinblue', option='cc_name')
        return message
    
    def send_on_successful_booking(self, activity: Activity):
 
        message = self.prepare_message()
        message.subject = 'Zdrofit -automatyczna rejestracja'
        text = (
                '<html><body>'
                '<h3>Zdrofit automatyczna rejestracja</h3>'
                f'<p>{self.user.get_first_name_vocative()},</p>'
                f'<p>Zapis na zajęcja <b>{activity.name}</b> odbywające się <b>{Weekday.name_pl_acc(activity.weekday)}</b> o godz. <b>{activity.hour}</b> w klubie <b>{activity.club_name}</b> zakończył się pomyślnie.<br/>'
                f'Pozycja na liście: <b>{activity.limit - activity.available + 1}</b>, liczba miejsc na zajęciach: <b>{activity.limit}</b></p>'
                '<p>Przybywaj i daj z siebie wszystko! :-)'
                '</body></html>'
        )
        message.content_html = text
        try:
            self.email.send_html_email(message)
        except SendInBlueEmailException as e:
            self.logger.error(f'Error sending email: {str(message)}')

    def send_on_activity_not_found(self, activity: Activity):
 
        message = self.prepare_message()
        message.subject = 'Zdrofit -automatyczna rejestracja - błąd rejestracji'
        text = (
                '<html><body>'
                '<h3>Zdrofit automatyczna rejestracja - problemik</h3>'
                f'<p>{self.user.get_first_name_vocative()},</p>'
                f'<p>Zapis na zajęcja <b>{activity.name}</b> odbywające się <b>{Weekday.name_pl_acc(activity.weekday)}</b> o godz. <b>{activity.hour}</b> w klubie <b>{activity.club_name}</b> nie powiódł się.</p>'
                 f'<p>Zajęcia nie występują w grafiku zajęć. Prawdopodobnie zostały odwołane ... </p>'
                '</body></html>'
        )
        message.content_html = text
        try:
            self.email.send_html_email(message)
        except SendInBlueEmailException as e:
            self.logger.error(f'Error sending email: {str(message)}')



    def send_on_max_retry_exceeded(self, activity: Activity, nr_of_retries: int):
 
        message = self.prepare_message()
        message.subject = 'Zdrofit -automatyczna rejestracja - błąd'
        text = (
                '<html><body>'
                '<h3>Zdrofit automatyczna rejestracja - problemik :(</h3>'
                f'<p>{self.user.get_first_name_vocative()},</p>'
                f'<p>Zapis na zajęcja <b>{activity.name}</b> odbywające się <b>{Weekday.name_pl_acc(activity.weekday)}</b> o godz. <b>{activity.hour}</b> w klubie <b>{activity.club_name}</b> nie powiódł się.<br/>'
                f'Wykonano {nr_of_retries} prób rejestracji, żadna z nich nie zakończyła się pomyślnie :-(</p>'
                '<p>Spróbuj ręcznego zapisu - może jeszcze się uda, zanim zabraknie miejsc ... </p>'
                '</body></html>'
        )
        message.content_html = text
        try:
            self.email.send_html_email(message)
        except SendInBlueEmailException as e:
            self.logger.error(f'Error sending email: {str(message)}')

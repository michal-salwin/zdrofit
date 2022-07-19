from blueemail.HtmlMessage import HtmlMessage
from booker.Activity import Activity
from booker.BookingStatsCollector import BookingStatsCollector
from booker.User import User
from utils.Weekday import Weekday
from blueemail.BaseEmail import BaseEmail

class EmailActivityNotFound(BaseEmail):

    def __init__(self, user: User, activity_to_book: Activity):
        super(). __init__(user)
        self.activity_to_book = activity_to_book

    def get_message(self) -> HtmlMessage:
        
        self.message.subject = 'GymBooker - automatyczna rejestracja - błąd rejestracji'
        text = (
                '<html><body>'
                '<h3>GymBooker automatyczna rejestracja - problemik</h3>'
                f'<p>{self.user.get_first_name_vocative()},</p>'
                f'<p>Zapis na zajęcja <b>{self.activity_to_book.name}</b> odbywające się <b>{Weekday.name_pl_acc(self.activity_to_book.weekday)}</b> o godz. <b>{self.activity_to_book.hour}</b> w klubie <b>{self.activity_to_book.club.get_name()}</b> nie powiódł się.</p>'
                f'<p>Zajęcia nie występują w grafiku zajęć. Prawdopodobnie zostały odwołane ... </p>'
                f'<p>Podjeliśmy próbę wyszukania innych zajęć w tym terminie - nie udało się jednak znaleźć zastępstwa.</p>'
                '</body></html>'
        )
        self.message.content_html = text  
        return self.message


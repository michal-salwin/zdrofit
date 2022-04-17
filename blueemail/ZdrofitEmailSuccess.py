from blueemail.HtmlMessage import HtmlMessage
from utils.Weekday import Weekday
from utils.RandomFileLineReader import RandomFileLineReader
from blueemail.BaseZdrofitEmail import BaseZdrofitEmail

class ZdrofitEmailSuccess(BaseZdrofitEmail):

    
    def get_message(self) -> HtmlMessage:
        random_line = RandomFileLineReader('email_variable_lines.txt')
        self.message.subject = 'Zdrofit -automatyczna rejestracja'
        text = (
                '<html><body>'
                '<h3>Zdrofit automatyczna rejestracja</h3>'
                f'<p>{self.user.get_first_name_vocative()},</p>'
                f'<p>Zapis na zajęcja <b>{self.activity.name}</b> odbywające się <b>{Weekday.name_pl_acc(self.activity.weekday)}</b> o godz. <b>{self.activity.hour}</b> w klubie <b>{self.activity.club.get_name()}</b> zakończył się pomyślnie.<br/>'
                f'Pozycja na liście: <b>{self.activity.limit - self.activity.available + 1}</b>, liczba miejsc na zajęciach: <b>{self.activity.limit}</b></p>'
                f'<p>{random_line.read_line()}</p>'
                '</body></html>'
        )
        self.message.content_html = text
        return self.message

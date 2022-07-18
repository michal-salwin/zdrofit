from blueemail.HtmlMessage import HtmlMessage
from blueemail.BaseEmail import BaseEmail
from utils.Weekday import Weekday
from utils.RandomFileLineReader import RandomFileLineReader

class EmailSuccess(BaseEmail):

    def get_message(self) -> HtmlMessage:
        random_line = RandomFileLineReader('email_variable_lines.txt')
        self.message.subject = 'GymBooker - automatyczna rejestracja'
        extra_line = ""
        if self.activity_booked.name != self.activity_to_book.name:
            extra_line = f'<p><b>Uwaga!</b> Zlecono zapis na zajęcia <b>{self.activity_to_book.name}</b>, jednak zajęcia te nie zostały znalezione w grafiku zajęć. Dokonaliśmy rezerwacji na inne zajęcia, które były dostępne w tym terminie.<p>'
        text = (
                '<html><body>'
                '<h3>GymBooker automatyczna rejestracja</h3>'
                f'<p>{self.user.get_first_name_vocative()},</p>'
                f'<p>Zapis na zajęcja <b>{self.activity_booked.name}</b> odbywające się <b>{Weekday.name_pl_acc(self.activity_booked.weekday)}</b> o godz. <b>{self.activity_booked.hour}</b> w klubie <b>{self.activity_booked.club.get_name()}</b> zakończył się pomyślnie.<br/>'
                f'Pozycja na liście: <b>{self.activity_booked.limit - self.activity_booked.available + 1}</b>, liczba miejsc na zajęciach: <b>{self.activity_booked.limit}</b></p>'
                + extra_line +
                f'<p>{random_line.read_line()}</p>'
                '</body></html>'
        )
        self.message.content_html = text
        return self.message

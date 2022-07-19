from blueemail.HtmlMessage import HtmlMessage
from blueemail.BaseEmail import BaseEmail
from booker.Activity import Activity
from booker.BookingStatsCollector import BookingStatsCollector
from booker.User import User
from utils.Weekday import Weekday
from utils.RandomFileLineReader import RandomFileLineReader

class EmailSuccess(BaseEmail):

    def __init__(self, user: User, activity_to_book: Activity, activity_booked: Activity, booking_stats_collector: BookingStatsCollector):
        super(). __init__(user)
        self.activity_to_book = activity_to_book
        self.activity_booked = activity_booked
        self.booking_stats = booking_stats_collector

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
                 f'<p>Zapisu udało się dokonać w trakcie <b>{self.booking_stats.get_nr_of_tries()}</b> próby o godzinie <b>{self.booking_stats.get_stop_time().strftime("%H:%M:%S")}</b><p>'
                f'<p>{random_line.read_line()}</p>'
                '</body></html>'
        )
        self.message.content_html = text
        return self.message

from blueemail.HtmlMessage import HtmlMessage
from booker.Activity import Activity
from booker.BookingStatsCollector import BookingStatsCollector
from booker.User import User
from utils.Weekday import Weekday
from blueemail.BaseEmail import BaseEmail

class EmailMaxRetryExceeded(BaseEmail):

    def __init__(self, user: User, activity_to_book: Activity, booking_stats_collector: BookingStatsCollector):
        super(). __init__(user)
        self.activity_to_book = activity_to_book
        self.booking_stats = booking_stats_collector

    def get_message(self) -> HtmlMessage:
        self.message.subject = 'GymBooker - automatyczna rejestracja - błąd'
        text = (
                '<html><body>'
                '<h3>GymBooker automatyczna rejestracja - problemik :(</h3>'
                f'<p>{self.user.get_first_name_vocative()},</p>'
                f'<p>Zapis na zajęcia <b>{self.activity_to_book.name}</b> odbywające się <b>{Weekday.name_pl_acc(self.activity_to_book.weekday)}</b> o godz. <b>{self.activity_to_book.hour}</b> w klubie <b>{self.activity_to_book.club.get_name()}</b> nie powiódł się.<br/>'
                f'<p>Wykonano <b>{self.booking_stats.get_nr_of_tries()}</b> prób  rejestracji pomiędzy godzinami <b>{self.booking_stats.get_start_time().strftime("%H:%M:%S")}</b> i <b>{self.booking_stats.get_stop_time().strftime("%H:%M:%S")}</b><p>'
                '<p>Spróbuj ręcznego zapisu - może jeszcze się uda zanim zabraknie miejsc ... </p>'
                '</body></html>'
        )
        self.message.content_html = text
        return self.message



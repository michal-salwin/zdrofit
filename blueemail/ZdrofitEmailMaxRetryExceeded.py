from blueemail.HtmlMessage import HtmlMessage
from utils.Weekday import Weekday
from blueemail.BaseZdrofitEmail import BaseZdrofitEmail

class ZdrofitEmailMaxRetryExceeded(BaseZdrofitEmail):

    def get_message(self) -> HtmlMessage:
        self.message.subject = 'Zdrofit -automatyczna rejestracja - błąd'
        text = (
                '<html><body>'
                '<h3>Zdrofit automatyczna rejestracja - problemik :(</h3>'
                f'<p>{self.user.get_first_name_vocative()},</p>'
                f'<p>Zapis na zajęcja <b>{self.activity.name}</b> odbywające się <b>{Weekday.name_pl_acc(self.activity.weekday)}</b> o godz. <b>{self.activity.hour}</b> w klubie <b>{self.activity.club.get_name()}</b> nie powiódł się.<br/>'
                f'Wykonano serię prób rejestracji, żadna nie zakończyła się pomyślnie :-(</p>'
                '<p>Spróbuj ręcznego zapisu - może jeszcze się uda, zanim zabraknie miejsc ... </p>'
                '</body></html>'
        )
        self.message.content_html = text
        return self.message



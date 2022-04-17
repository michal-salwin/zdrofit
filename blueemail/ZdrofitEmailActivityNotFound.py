from blueemail.HtmlMessage import HtmlMessage
from utils.Weekday import Weekday
from blueemail.BaseZdrofitEmail import BaseZdrofitEmail

class ZdrofitEmailActivityNotFound(BaseZdrofitEmail):

    def get_message(self) -> HtmlMessage:
        
        self.message.subject = 'Zdrofit -automatyczna rejestracja - błąd rejestracji'
        text = (
                '<html><body>'
                '<h3>Zdrofit automatyczna rejestracja - problemik</h3>'
                f'<p>{self.user.get_first_name_vocative()},</p>'
                f'<p>Zapis na zajęcja <b>{self.activity.name}</b> odbywające się <b>{Weekday.name_pl_acc(self.activity.weekday)}</b> o godz. <b>{self.activity.hour}</b> w klubie <b>{self.activity.club.get_name()}</b> nie powiódł się.</p>'
                f'<p>Zajęcia nie występują w grafiku zajęć. Prawdopodobnie zostały odwołane ... </p>'
                '</body></html>'
        )
        self.message.content_html = text  
        return self.message


from blueemail.BaseEmail import BaseEmail
from blueemail.HtmlMessage import HtmlMessage
from app_config.AppConfig import AppConfig
from app_logger.AppLogger import AppLogger
from exceptions.SendInBlueEmailException import SendInBlueEmailException
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from blueemail.HtmlMessage import HtmlMessage
from exceptions.SendInBlueEmailException import SendInBlueEmailException
class EmailSender:

    message: HtmlMessage = None

    def __init__(self):

        self.config = AppConfig()
        self.logger = AppLogger()
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = self.config.get(section='sendinblue', option='api_key')
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    def send(self, message: HtmlMessage):
        try:
            self.send_html_email(message)
        except SendInBlueEmailException as e:
            self.logger.error(f'Error sending email: {str(message)} {e}')

    def send_html_email(self, message: HtmlMessage):

        sender = {"name":message.from_name,"email":message.from_email}
        to = [{"email":message.to_email,"name":message.to_name}]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(sender=sender, to=to, html_content=message.content_html, subject=message.subject)
        if message.cc_email != '':
            send_smtp_email.cc = [{"email":message.cc_email,"name":message.cc_name}]
        if message.bcc_email != '':
            send_smtp_email.bcc = [{"email":message.bcc_email,"name":message.bcc_name}]

        try:
            api_response = self.api_instance.send_transac_email(send_smtp_email)
        except ApiException as e:
            raise SendInBlueEmailException(f'SendInBlue ApiException: to: {message.to_email}, status: {e.status}, reason: {e.reason}, body: {e.body}')
        except Exception as e:
            raise SendInBlueEmailException(f'SendInBlue Exception: {e}')
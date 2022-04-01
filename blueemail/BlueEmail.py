from asyncio.log import logger
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from blueemail.HtmlMessage import HtmlMessage
from log.Logger import Logger

class BlueEmail:
    api_instance = None

    def __init__(self,api_key: str, logger: Logger):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        self.logger = logger

    def send_html_email(self, message: HtmlMessage):    

        sender = {"name":message.from_name,"email":message.from_email}
        to = [{"email":message.to_email,"name":message.to_name}]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=message.content_html, sender=sender, subject=message.subject)

        try:
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            self.logger.info (f'SendInBlue message to {message.to_email} has been sent successfully')
        except ApiException as e:
            self.logger.error(f'SendInBlue ApiException: to: {message.to_email}, status: {e.status}, reason: {e.reason}')
        except Exception as e:
            self.logger.error(f'SendInBlue Exception: {e}')
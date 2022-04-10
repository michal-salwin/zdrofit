from exceptions.Error import Error

class SendInBlueEmailException(Error):
    """Raised when there is a problem with sending mail via BlueMail
    Attributes:
        response_code    -- http response code
        response_content -- http content
        message          -- explanation of the error
    """

    def __init__(self, message="Sending mail failed!"):
        self.message = message
        super().__init__(self.message)

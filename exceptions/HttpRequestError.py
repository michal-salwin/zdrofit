from exceptions.Error import Error

class HttpRequestError(Error):
    """Raised when there is a problem with autenthication
    Attributes:
        response_code    -- http response code
        response_content -- http content
        message          -- explanation of the error
    """

    def __init__(self,url: str,code: int, reason: str, content, message="HTTP request failed!"):
        self.url = url
        self.code = code
        self.reason = reason
        self.content = content
        self.message = message + f' (url: {url}, code: {code}, reason: {reason}, content: {str(content)})'
        super().__init__(self.message)

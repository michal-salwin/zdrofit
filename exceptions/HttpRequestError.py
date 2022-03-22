from exceptions.Error import Error

class HttpRequestError(Error):
    """Raised when there is a problem with autenthication
    Attributes:
        response_code    -- http response code
        response_content -- http conten
        message          -- explanation of the error
    """

    def __init__(self,url,response_code, response_content, message="HTTP request failed!"):
        self.url = url
        self.response_code = response_code
        self.response_content = response_content
        self.message = message + f' (url: {url}, code: {response_code}, content: {str(response_content)})'
        super().__init__(self.message)

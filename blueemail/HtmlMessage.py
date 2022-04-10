class HtmlMessage:
    from_email: str = None
    from_name: str = None
    to_email: str = None
    to_name: str = None
    cc_email: str = None
    cc_name: str = None
    subject: str = None
    content_html: str = None

    def __str__(self):
        return f'Email to: {self.to_email}, subject: {self.subject}'


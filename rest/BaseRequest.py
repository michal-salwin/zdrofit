from requests import Response
import requests

class BaseRequest:

    cookies: dict = dict()

    base_url: str = 'https://zdrofit.perfectgym.pl/'
    
    def login(self, uri:str,data) -> Response:
        response = requests.post(self.base_url+uri, data=data)
        self.cookies = response.cookies
        return response

    def post(self, uri:str,data) -> Response:
        response = requests.post(self.base_url+uri, data=data, cookies=self.cookies)
        return response

    def get(self, uri:str) -> Response:
        response = requests.get(self.base_url+uri, cookies=self.cookies)
        return response
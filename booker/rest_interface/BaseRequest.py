import json
from requests import Response
import requests

class BaseRequest:

    cookies: dict = dict()
    headers: dict = dict()
    base_url: str 
    proxies = {}

    def login(self, uri:str,data) -> Response:
        response = requests.post(self.base_url+uri, json=data, headers=self.headers, proxies=self.proxies)
        self.cookies = response.cookies
        return response

    def post(self, uri:str,data) -> Response:
        response = requests.post(self.base_url+uri, data=data, cookies=self.cookies, headers=self.headers, proxies=self.proxies)
        return response

    def post_json(self, uri:str,json) -> Response:
        response = requests.post(self.base_url+uri,json=json, cookies=self.cookies, headers=self.headers, proxies=self.proxies)
        return response

    def get(self, uri:str) -> Response:
        response = requests.get(self.base_url+uri, cookies=self.cookies, headers=self.headers, proxies=self.proxies)
        return response

    def set_base_url(self, url: str) -> None:
        self.base_url = url

    def add_header(self, key: str, value: str) -> None: 
        self.headers[key] = value
    

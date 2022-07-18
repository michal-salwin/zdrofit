import codecs
import configparser

class AppConfig (object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AppConfig, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__conf = configparser.ConfigParser()
        self.__conf.read_file(codecs.open('gymbooker.ini','r','UTF8'))
    
    def get(self, section: str, option: str):
        return self.__conf.get(section=section,option=option)

    def get_account_param(self, account: str, option: str):
        return self.__conf.get(section=f'account.{account}',option=option)
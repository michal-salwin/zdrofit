import configparser

class AppConfig:
   
    def __init__(self, config_file: str):
        self.__conf = configparser.ConfigParser()
        self.__conf.read(config_file)
    
    def get(self, section: str, option: str):
        return self.__conf.get(section=section,option=option)

    def get_account_param(self, account: str, option: str):
        return self.__conf.get(section=f'zdrofit.account.{account}',option=option)
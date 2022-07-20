from app_config.AppConfig import AppConfig

class User:
    __initials:       str = None
    __first_name:     str = None
    __surname:        str = None
    __email:          str = None
    __login:          str = None
    __password:       str = None
    __first_name_voc: str = None
 
    def __init__(self,initials, config: AppConfig):
        self.__initials = initials
        self.__first_name =     config.get_account_param(initials,'first_name')
        self.__surname =        config.get_account_param(initials,'surname')
        self.__email =          config.get_account_param(initials,'email')
        self.__login =          config.get_account_param(initials,'login')
        self.__password =       config.get_account_param(initials,'password')
        self.__first_name_voc=  config.get_account_param(initials,'first_name_vocative')  

    def __str__(self):
         return str('{:<4} {:<12} {:<15}'.
            format(self.__initials, 
                   self.__first_name, 
                   self.__surname
            )
    )

    def get_first_name(self) -> str:
        return self.__first_name

    def get_first_name_vocative(self) -> str:
        return self.__first_name_voc

    def get_surname(self) -> str:
        return self.__surname

    def get_fullname(self)->str:
        return f'{self.__first_name} {self.__surname}'

    def get_initials(self)->str:
        return self.__initials

    def get_email(self)->str:
        return self.__email

    def get_login(self)->str:
        return self.__login

    def get_password(self)->str:
        return self.__password
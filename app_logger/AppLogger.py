import logging

class AppLogger:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AppLogger, cls).__new__(cls)
        return cls.instance

    def __init__(self):
         logging.basicConfig(filename='scrapper.log',
                            filemode='a',
                            format='%(asctime)s - %(message)s', 
                            level=logging.INFO)
    
    def info(self,message):
        logging.info(message)


    def error(self,message):
        logging.info(message)


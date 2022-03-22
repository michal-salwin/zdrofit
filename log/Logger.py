import logging

class Logger:
   
    def __init__(self):
         logging.basicConfig(filename='scrapper.log',
                            filemode='a',
                            format='%(asctime)s - %(message)s', 
                            level=logging.INFO)
    
    def info(self,message):
        logging.info(message)


    def error(self,message):
        logging.info(message)


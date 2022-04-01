import logging

class Logger:
   
    def __init__(self, log_file):
         logging.basicConfig(filename=log_file,
                            filemode='a',
                            format='%(asctime)s - %(message)s', 
                            level=logging.INFO)
    
    def info(self,message):
        logging.info(message)


    def error(self,message):
        logging.info(message)


from zdrofit.RestConsumer import Scrapper

scrapper = Scrapper('AT')
scrapper.get_activities(32,weekday="Wednesday")


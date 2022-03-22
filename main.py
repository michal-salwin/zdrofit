from ZdrofitScrapper import ZdrofitScrapper

scrapper = ZdrofitScrapper('michal.salwin@gmail.com','password')
# 33 - Gdańsk Przymorze
# 43  - Gdynia Chawarzno
# 32 - Gdańsk Manhattan

#scrapper.get_activities(43,activity_list=('Shape','Brzuch i Stretch'))
#scrapper.cancel_booking(33,"TBC")
scrapper.book_activity(32,"Trening Obwodowy",retry_nr=10, seconds_between_retry=2)
#$scrapper.get_activities(32,bookable_only=False)
#scrapper.get_activities(32)
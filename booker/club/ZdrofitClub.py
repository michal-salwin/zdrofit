from booker.club.Club import Club

class ZdrofitClub(Club):

    def __init__(self, symbol: str):
        self.symbol = symbol.lower()
        self.clubs = {
        'gdansk-przymorze':       (33,'Gdańsk Przymorze'),
        'gdansk-manhattan':       (32,'Gdańsk Manhattan'),
        'gdynia-chwarzno':        (43,'Gdynia Chwarzno'),
        'gdynia-karwiny':         (65,'Gdynia Karwiny'),
        'gdynia-riviera':         (37,'Gdynia Riviera'),
        'gdynia-plac-kaszubski':  (76,'Gdynia Plac Kaszubski')
    }


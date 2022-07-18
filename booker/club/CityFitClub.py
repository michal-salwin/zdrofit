from booker.club.Club import Club

class CityFitClub(Club):

    def __init__(self, symbol: str):
        self.symbol = symbol.lower()
        self.clubs = {
        'gdansk-forum':       (100049,'Gdańsk Forum')
    }


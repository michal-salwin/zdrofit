class Club:

    __clubs = {
        'gdansk-przymorze': (33,'Gdańsk Przymorze'),
        'gdansk-manhattan': (32,'Gdańsk Manhattan'),
        'gdynia-chwarzno':  (43,'Gdynia Chwarzno')
    }

    __symbol: str = None

    def __init__(self, symbol: str):
        self.__symbol = symbol.lower()
    
    def get_id(self) -> str:
        return str(self.__clubs[self.__symbol][0])

    def get_name(self) -> str:
        return str(self.__clubs[self.__symbol][1])

    def get_symbol(self) -> str:
        return self.__symbol


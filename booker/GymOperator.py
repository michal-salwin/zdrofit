class GymOperator:

    __operators = {
        'zdrofit':                ('Zdrofit')
    }

    __symbol: str = None

    def __init__(self, symbol: str):
        self.__symbol = symbol.lower()

    def get_name(self) -> str:
        return str(self.__clubs[self.__symbol][0])

    def get_symbol(self) -> str:
        return self.__symbol


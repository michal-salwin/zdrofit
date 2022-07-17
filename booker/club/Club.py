from abc import ABC, abstractmethod

class Club:

    symbol: str = None
    clubs: dict

    def __init__(self, symbol: str):
        self.symbol = symbol.lower()
    
    def get_id(self) -> str:
        return str(self.clubs[self.symbol][0])

    def get_name(self) -> str:
        return str(self.clubs[self.symbol][1])

    def get_symbol(self) -> str:
        return self.symbol
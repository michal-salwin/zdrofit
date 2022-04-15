import random
class RandomFileLineReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name

    def read_line(self) -> str:
        with open(self.__file_name,'r',encoding='UTF-8') as file:
            line = next(file)
            for num, aline in enumerate(file, 2):
                if random.randrange(num):
                    continue
                line = aline
            return line

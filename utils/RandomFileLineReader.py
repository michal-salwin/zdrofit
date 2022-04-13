import random
import os

class RandomFileLineReader:

    def __init__(self):
        pass

    def read_line(self, file_name: str) -> str:
        with open(file_name,'r') as file:
            line = next(file)
            for num, aline in enumerate(file, 2):
                if random.randrange(num):
                    continue
                line = aline
            return line

r = RandomFileLineReader()
line = r.read_line('file.txt')
print(line)

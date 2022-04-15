class Weekday:

    names_pl: dict = {
        'monday':   ('Poniedziałek','Monday', 'Poniedziałku','w najbliższy poniedziałek'),
        'tuesday':  ('Wtorek','Tuesday','Wtorku','w najbliższy wtorek'),
        'wednesday':('Środa','Wednesday', 'Środy','w najbliższą środę'),
        'thursday': ('Czwartek','Thursday','Czwartku', 'w najbliższy czwartek'),
        'friday':   ('Piątek','Friday','Piątku', 'w najbliższy piątek'),
        'saturday': ('Sobota','Saturday','Soboty','w najbliższą sobotę'),
        'sunday':   ('Niedziela','Sunday','Niedzieli','w najbliższą niedzielę')
    }

    @staticmethod
    def name_pl(weekday: str) -> str:
        return str(Weekday.names_pl[weekday.lower()][0])

    @staticmethod
    def name_ang(weekday: str) -> str:
        return str(Weekday.names_pl[weekday.lower()][1])

    @staticmethod
    def name_pl_gen(weekday: str) -> str:
        return str(Weekday.names_pl[weekday.lower()][2])

    @staticmethod
    def name_pl_acc(weekday: str) -> str:
        return str(Weekday.names_pl[weekday.lower()][3])


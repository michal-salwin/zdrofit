class Person:

    def __init__(self):
        self.contacts = {
            "domowy": "12345",
            "sluzbowy": "56789"
        };
        
    def printContacts(self):
        for item in self.contacts:
            print ('type: %s, value: %s', (item, self.contacts[item]))

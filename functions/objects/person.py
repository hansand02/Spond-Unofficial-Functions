class Person:
    def __init__(self, name):
        self.name = name
        self.accepted = 0
        self.declined = 0
        self.unanswered = 0
        self.unconfirmed = 0
        self.waitinglist = 0

        self.first_practice = None
        self.last_practice = None

    def __str__(self):
        return f"{self.name} has attended {self.accepted} practices."
    
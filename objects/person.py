class Person:
    def __init__(self, name):
        self.name = name
        self.practices_attended = 0
        self.first_practice = None
        self.last_practice = None

    def __str__(self):
        return f"{self.name} has attended {self.practices_attended} practices."
    
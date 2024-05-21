from enum import Enum


class Role(Enum):
    ADMIN = 'admin'
    QA = 'quality manager'
    SME = 'subject matter expert'


class User:
    def __init__(self, name, surname=None, email=None, roles=None):
        if roles is None:
            roles = []
        self.name = name
        self.surname = surname
        self.email = email
        self.roles = roles

    def __str__(self):
        return self.print()

    def __lt__(self, other):
        return self.print() == other.print()

    def __eq__(self, other):
        return self.print() == other

    def __repr__(self):
        return self.print()

    def print(self):
        if self.surname is None:
            return self.name
        else:
            return f'{self.surname} {self.name}'

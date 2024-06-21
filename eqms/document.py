import uuid
from datetime import date

from eqms.user import User, Role


class Document:
    def __init__(
            self,
            text: str,
            name: str = '',
            version: int = 1,
            author: str | User = None,
            effective: date = None,
            withdrawn: date = None,
            signed_by: tuple = (),
            withdrawn_by: tuple = (),
            _uuid: int = None,
    ):
        if _uuid is None:
            self.uuid = uuid.uuid4().int
        else:
            self.uuid = _uuid
        self.text = text
        self.version = version
        self.name = name
        self.author = author
        self.effective = effective
        self.withdrawn = withdrawn
        self.signed_by = signed_by
        self.withdrawn_by = withdrawn_by
        if name == '':
            self.name = text[:20]

    def sign(self, signing_person: User):
        if can_perform_the_task(signing_person):
            self.signed_by = self.signed_by + (signing_person,)
            self.effective = date.today()
            return True
        else:
            return False

    def withdraw(self, withdraw_person: User):
        if can_perform_the_task(withdraw_person):
            self.withdrawn_by = self.withdrawn_by + (withdraw_person,)
            self.withdrawn = date.today()
            return True
        else:
            return False

    def print(self):
        return f'''
| Key       | Value                                     |
| --------- | ----------------------------------------- |
| Name      | {self.name}                               |
| Author    | {self.author}                             |
| Effective | {self.effective.strftime('%Y %m %d')}     |
| Withdrawn | {self.withdrawn.strftime('%Y %m %d')}     |
| Signed By | {self.signed_by}                          | 

{self.text}
'''.strip()


def can_perform_the_task(person: User):
    if Role.ADMIN in person.roles:
        return True
    elif Role.QA in person.roles:
        return True
    else:
        return False

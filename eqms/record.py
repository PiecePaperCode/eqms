import uuid
from datetime import datetime

from eqms.user import User


class Record:
    def __init__(
            self,
            description,
            execution=None,
            executed_by=None,
            executed_at=None,
            _uuid=uuid.uuid4().int
    ):
        self._uuid = _uuid
        self.description = description
        self.execution = execution
        self.executed_by = executed_by
        self.executed_at = executed_at

    def execute(self, execution_description: str, executed_by: User):
        if self.executed_at is not None:
            raise Exception("You cant execute an already executed record")
        self.execution = execution_description
        self.executed_by = executed_by
        self.executed_at = datetime.now().date()

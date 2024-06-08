import uuid
from datetime import datetime
from enum import Enum

from eqms.user import User


class RecordType(Enum):
    CHANGE_REQUEST = 'CHANGE_REQUEST'
    DEVIATION = 'DEVIATION'
    TRAINING = 'TRAINING'
    TEST_REPORT = 'TEST_REPORT'


class Record:
    def __init__(
            self,
            description,
            record_type=None,
            execution=None,
            executed_by=None,
            executed_at=None,
            _uuid=uuid.uuid4().int
    ):
        self._uuid = _uuid
        self.type: RecordType | None = None
        self.description = description
        self.execution_evidence = execution
        self.executed_by = executed_by
        self.executed_at = executed_at

    def execute(self, execution_description: str, executed_by: User):
        if self.executed_at is not None:
            raise Exception("You cant execute an already executed record")
        self.execution_evidence = execution_description
        self.executed_by = executed_by
        self.executed_at = datetime.now().date()

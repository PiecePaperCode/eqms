import unittest
from datetime import datetime

from eqms.record import Record, RecordType
from eqms.user import User, Role


class TestRecord(unittest.TestCase):
    def setUp(self):
        self.record = Record("the description of the record")

    def test_creating_a_record(self):
        self.assertEqual("the description of the record", self.record.description)

    def test_execute_a_record(self):
        self.record.execute("I did it", User("Michael Scott", roles=[Role.QA]))
        self.assertEqual("I did it", self.record.execution)
        self.assertEqual("Michael Scott", self.record.executed_by)
        self.assertEqual(datetime.now().date(), self.record.executed_at)

    def test_record_execution_can_only_be_run_once(self):
        self.record.execute("I did it", User("Michael Scott", roles=[Role.QA]))
        self.assertRaises(
            Exception,
            self.record.execute, "I did it", User("Michael Scott")
        )

    def test_record_can_be_of_a_certain_type(self):
        self.record.type = RecordType.TRAINING
        self.assertEqual(self.record.type, RecordType.TRAINING)


if __name__ == '__main__':
    unittest.main()

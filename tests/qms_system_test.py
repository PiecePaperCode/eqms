import unittest

from eqms.document import Document
from eqms.eqms import eQMS


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.eqms = eQMS('Dunder Mifflin')

    def test_create_eQMS(self):
        self.assertEqual(self.eqms.name, 'Dunder Mifflin')

    def test_should_contain_qms_project(self):
        self.eqms.initialize_qms_project()
        self.assertGreater(len(self.eqms.qms_documents.generate_overview()), 0)


if __name__ == '__main__':
    unittest.main()

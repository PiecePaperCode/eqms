import unittest

from eqms.document import Document
from eqms.eqms import eQMS


class MyTestCase(unittest.TestCase):
    def test_eQMS(self):
        eqms = eQMS('Dunder Mifflin')
        document = Document("My document")
        eqms.document_store.add_document(document)
        self.assertEqual(eqms.document_store.get_document(document.uuid).uuid, document.uuid)


if __name__ == '__main__':
    unittest.main()

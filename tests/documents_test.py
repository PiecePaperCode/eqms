import unittest
from datetime import datetime

from eqms.document import Document
from eqms.user import User, Role


class DocumentTests(unittest.TestCase):
    def setUp(self):
        self.document = Document(
            '# Hi i am a Document \n text...',
            version=1,
            name='My Document',
            author='John Doe',
            effective=datetime(2020, 1, 1),
            withdrawn=datetime(2021, 1, 1),
            signed_by=(User('Pam Beesly'), User('Jim Halpert'))
        )

    def test_creating_a_document(self):
        self.assertEqual(self.document.text, '# Hi i am a Document \n text...')
        self.assertEqual(self.document.version, 1)
        self.assertEqual(self.document.author, User('John Doe'))
        self.assertEqual(self.document.name, 'My Document')
        self.assertEqual(self.document.effective, datetime(2020, 1, 1))
        self.assertEqual(self.document.withdrawn, datetime(2021, 1, 1))
        self.assertEqual(
            self.document.signed_by,
            (User('Pam Beesly'), User('Jim Halpert'))
        )

    def test_signing_a_document(self):
        self.document.sign(User('Michael Scott', roles=[Role.QA]))
        self.assertEqual(self.document.signed_by[2], 'Michael Scott')
        self.assertEqual(self.document.effective, datetime.today().date())

    def test_signing_a_document_with_wrong_role(self):
        self.document.sign(User('Michael Scott', roles=[Role.SME]))
        self.assertEqual(len(self.document.signed_by), 2)
        self.assertEqual(self.document.effective, datetime(2020, 1, 1))

    def test_withdrawing_a_document(self):
        self.document.withdraw(User('Michael Scott', roles=[Role.QA]))
        self.assertEqual(self.document.withdrawn_by[0], User('Michael Scott'))
        self.assertEqual(self.document.withdrawn, datetime.today().date())

    def test_printing_a_document(self):
        printed_document = self.document.print()
        self.assertEqual(
            printed_document,
            '''| Key       | Value                                     |
| --------- | ----------------------------------------- |
| Name      | My Document                               |
| Author    | John Doe                             |
| Effective | 2020 01 01     |
| Withdrawn | 2021 01 01     |
| Signed By | (Pam Beesly, Jim Halpert)                          | 

# Hi i am a Document 
 text...'''
        )


if __name__ == '__main__':
    unittest.main()

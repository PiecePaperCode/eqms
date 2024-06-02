import unittest

from eqms.document import Document
from eqms.document_store import Store
from eqms.user import User, Role


class TestDocumentStore(unittest.TestCase):
    def setUp(self):
        self.store = Store()

    def test_add_document_to_store(self):
        document = Document("text...")
        self.store.add_document(document)
        self.assertEqual(self.store.count_total_documents(), 1)
        self.assertEqual(
            self.store.get_document(document.uuid).text,
            "text..."
        )

    def test_retrieve_document_from_store(self):
        document = Document("text...", name="doc1")
        self.store.add_document(document)
        self.assertEqual(
            self.store.get_document(document.uuid).name,
            "doc1"
        )

    def test_overview_document_from_store(self):
        document = Document("text...", name="doc1")
        self.store.add_document(document)
        self.assertEqual(self.store.generate_overview()[0].uuid, document.uuid)
        self.assertEqual(self.store.generate_overview()[0].name, "doc1")
        self.assertEqual(self.store.generate_overview()[0].author, None)

    def test_withdraw_document_overview_from_store(self):
        document = Document("text...", name="doc1")
        document.withdraw(User('Tom Scott', roles=[Role.QA]))
        self.store.add_document(document)
        self.assertEqual(len(self.store.generate_overview()), 0)
        self.assertEqual(
            len(self.store.generate_overview(include_withdrawn=True)),
            1
        )

    def test_folder_in_store(self):
        self.assertEqual(len(self.store.folders), 0)

    def test_add_folder_to_store(self):
        self.store.add_folder('QMS')
        self.assertEqual(len(self.store.folders), 1)

    def test_remove_folder_to_store(self):
        self.store.add_folder('QMS')
        self.assertEqual(len(self.store.folders), 1)
        self.store.remove_folder('QMS')
        self.assertEqual(len(self.store.folders), 0)

    def test_add_remove_document_from_folder(self):
        self.store.add_folder('QMS')
        document = Document("Best SOP ever", name="01 SOP Quality")
        self.store.add_document(document)
        self.store.add_document_to_folder(document.name, "QMS")
        self.assertEqual(len(self.store.folders["QMS"].documents), 1)
        self.store.remove_document_from_folder(document.name, "QMS")
        self.assertEqual(len(self.store.folders["QMS"].documents), 0)

    def test_overview_documents_from_folder(self):
        self.store.add_folder('QMS')
        document = Document("Best SOP ever", name="01 SOP Quality")
        self.store.add_document(document)
        self.store.add_document_to_folder(document.name, "QMS")
        self.assertEqual(
            self.store.generate_overview(folder="QMS")[0].name,
            "01 SOP Quality"
        )

    def test_add_newer_version_of_document(self):
        document = Document("Best SOP ever", name="01 SOP Quality")
        self.store.add_document(document)
        self.assertEqual(len(self.store.documents[document.uuid]), 1)
        document2 = Document(
            "even Better",
            name=document.name,
            version=99,
            _uuid=document.uuid
        )
        self.store.add_document(document2)
        self.assertEqual(len(self.store.documents[document.uuid]), 2)
        self.assertEqual(len(self.store.get_versions(document.uuid)), 2)
        self.assertEqual(
            self.store.get_document(document.uuid, version=2).version,
            2
        )

    def test_wrong_version_of_document(self):
        document = Document("Best SOP ever", name="01 SOP Quality")
        self.store.add_document(document)
        self.assertRaises(
            Exception,
            self.store.get_document, document.uuid, version=99
        )


if __name__ == '__main__':
    unittest.main()

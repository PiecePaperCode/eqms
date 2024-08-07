import unittest
from copy import deepcopy

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

    def test_lifecycle_of_documents(self):
        qa = User('Tom Scott', roles=[Role.QA])
        document = Document("text...", name="doc1")
        self.store.add_document(document)
        self.store.sign(document.uuid, qa)
        document2 = Document("New Text2", name="doc2", _uuid=document.uuid)
        self.store.add_document(document2)
        document3 = Document("New Text3", name="doc3")
        self.store.update_document(document2.uuid, document3)
        self.store.sign(document.uuid, qa)
        self.assertEqual(
            self.store.get_document(document.uuid, version=2).signed_by,
            (qa,)
        )
        self.assertEqual(
            self.store.get_document(document.uuid, version=2).withdrawn_by,
            ()
        )
        self.assertEqual(
            self.store.get_document(document.uuid, version=1).signed_by,
            (qa,)
        )
        self.assertEqual(
            self.store.get_document(document.uuid, version=1).withdrawn_by,
            (qa,)
        )
        self.assertEqual(
            self.store.get_document(document.uuid, version=2).text,
            "New Text3"
        )
        self.assertEqual(
            self.store.get_document(document.uuid, version=2).version,
            2
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
        self.store.sign(document.uuid, User('Tom Scott', roles=[Role.QA]))
        self.assertEqual(len(self.store.documents[document.uuid]), 1)
        document2 = deepcopy(document)
        self.store.add_document(document2)
        self.assertEqual(len(self.store.documents[document.uuid]), 2)
        self.assertEqual(len(self.store.get_versions(document.uuid)), 2)
        self.assertEqual(
            self.store.get_document(document.uuid, version=2).version,
            2
        )
        self.assertEqual(
            self.store.get_document(document.uuid, version=2).signed_by,
            ()
        )

    def test_updating_draft_document(self):
        document = Document("Best SOP ever", name="01 SOP Quality")
        self.store.add_document(document)
        document2 = Document(
            "Best SOP ever 2",
            name=document.name,
        )
        it_worked = self.store.update_document(document.uuid, document2)
        self.assertTrue(it_worked)
        self.assertEqual(self.store.get_document(document.uuid).version, 1)
        self.assertEqual(
            self.store.get_document(document.uuid).text,
            "Best SOP ever 2"
        )

    def test_updating_effective_document_should_not_be_possible(self):
        document = Document("Best SOP ever", name="01 SOP Quality")
        self.store.add_document(document)
        self.store.sign(document.uuid, User('Tom Scott', roles=[Role.QA]))
        document2 = Document(
            "Best SOP ever 2",
            name=document.name,
        )
        it_worked = self.store.update_document(document.uuid, document2)
        self.assertFalse(it_worked)
        self.assertEqual(
            self.store.get_document(document.uuid).text,
            "Best SOP ever"
        )

    def test_wrong_version_of_document(self):
        document = Document("Best SOP ever", name="01 SOP Quality")
        self.store.add_document(document)
        self.assertRaises(
            Exception,
            self.store.get_document, document.uuid, version=99
        )

    def test_get_all_versions_of_document(self):
        document = Document("Best SOP ever", name="01 SOP Quality", version=1)
        self.store.add_document(document)
        self.store.sign(document.uuid, User('Tom Scott', roles=[Role.QA]))
        document2 = Document("Best SOP ever", name="01 SOP Quality", version=2, _uuid=document.uuid)
        self.store.add_document(document2)
        self.assertEqual(self.store.get_versions(document.uuid), [1, 2])

    def test_new_version_of_document_on_top_of_not_signed_document(self):
        document = Document("Best SOP ever", name="01 SOP Quality", version=1)
        self.store.add_document(document)
        document2 = Document("Best SOP ever", name="01 SOP Quality", version=2, _uuid=document.uuid)
        it_worked = self.store.add_document(document2)
        self.assertFalse(it_worked)


if __name__ == '__main__':
    unittest.main()

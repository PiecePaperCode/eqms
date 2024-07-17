import copy

from eqms.document import Document
from eqms.document_store import Store
from eqms.user import User, Role


class eQMS:
    def __init__(self, name):
        self.name = name
        self.qms_documents = Store()

    def initialize_qms_project(self):
        documents = [
            {'name': '01 Manual - Quality Manual', 'folder': 'Policy'},
            {'name': '01 SOP - Document and Record Lifecycle', 'folder': 'SOP'},
            {'name': '02 SOP - Risk Management', 'folder': 'SOP'},
            {'name': '03 SOP - Software Development Lifecycle', 'folder': 'SOP'},
        ]
        for document in documents:
            doc = Document(
                'Text',
                name=document['name'],
                author=User('Michael Scott')
            )
            doc.sign(User('Michael Scott', roles=[Role.QA]))
            self.qms_documents.add_document(doc)
            doc2 = Document(
                'Text',
                name=document['name'],
                author=User('Michael Scott'),
                version=2,
                _uuid=doc.uuid
            )
            self.qms_documents.add_document(doc2)
            if document['folder'] not in self.qms_documents.folders.keys():
                self.qms_documents.add_folder(document['folder'])
            self.qms_documents.folders[document['folder']].add_document(doc)

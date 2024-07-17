from datetime import datetime

from eqms.document import Document
from eqms.user import User


class Store:
    def __init__(self, documents=None, folder=None):
        if documents is None:
            documents = {}
        self.documents: dict = documents
        if folder is None:
            folder = {}
        self.folders: dict = folder

    def add_document(self, document):
        if document.uuid not in self.documents:
            document.version = 1
            self.documents[document.uuid] = {document.version: document}
        else:
            document.version = len(self.documents[document.uuid]) + 1
            self.documents[document.uuid][document.version] = document

    def get_document(self, uuid, version=None) -> Document:
        if version is None:
            return self.documents[uuid][max(self.get_versions(uuid))]
        elif version not in self.documents[uuid]:
            raise Exception(f"Version {version} not found in document {uuid}")
        else:
            return self.documents[uuid][version]

    def update_document(self, uuid, document):
        old_document = self.get_document(uuid)
        if old_document.effective is not None:
            return False
        document.uuid = old_document.uuid
        document.version = old_document.version
        self.documents[uuid][document.version] = document
        return True

    def sign(self, uuid, user: User):
        document = self.get_document(uuid)
        document.sign(user)
        for version in self.get_versions(uuid)[:-1]:
            self.documents[uuid][version].withdraw(user)

    def get_versions(self, uuid) -> list:
        return list(self.documents[uuid].keys())

    def count_total_documents(self):
        return len(self.documents)

    def generate_overview(self, include_withdrawn=False, folder=None):
        overview = []

        class MetaData:
            def __init__(
                    self,
                    uuid: int,
                    name: str,
                    author: str,
                    effective: datetime.date,
                    withdrawn: datetime.date,
            ):
                self.uuid = uuid
                self.name = name
                self.author = author
                self.effective = effective
                self.withdrawn = withdrawn

        for uuid in self.documents.keys():
            document = self.get_document(uuid)
            if document.withdrawn is not None and not include_withdrawn:
                continue

            if (folder is not None
                    and document.name not in self.folders[folder].documents):
                continue

            overview.append(
                MetaData(
                    document.uuid,
                    document.name,
                    document.author,
                    document.effective,
                    document.withdrawn,
                )
            )
        return overview

    def add_folder(self, name):
        self.folders[name] = Folder(name)

    def remove_folder(self, name):
        del self.folders[name]

    def add_document_to_folder(self, document_name, folder):
        self.folders[folder].add_document(document_name)

    def remove_document_from_folder(self, name, folder):
        self.folders[folder].remove_document(name)


class Folder:
    def __init__(self, name, documents: list[str] = None):
        self.name = name
        if documents is None:
            documents = []
        self.documents: list[str] = documents

    def add_document(self, document: str):
        self.documents.append(document)

    def remove_document(self, document: str):
        self.documents.remove(document)

    def __lt__(self, other):
        return self.name == other.name

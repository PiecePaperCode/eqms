from eqms.document_store import Store

class eQMS:
    def __init__(self, name):
        self.name = name
        self.document_store = Store()


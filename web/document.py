from web.view import eqms


def create_new_version_of_document(document_id) -> bool:
    document = eqms.qms_documents.get_document(document_id)
    new_version = document.increment_version()
    it_worked = eqms.qms_documents.add_document(new_version)
    return it_worked
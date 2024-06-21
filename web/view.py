from django.shortcuts import render
from eqms.eqms import eQMS

eqms = eQMS('Dunder Mifflin')
eqms.initialize_qms_project()


def index(request):
    return render(
        request,
        'base.html',
        {
            'eqms': eqms,
        }
    )


def render_document(request, document_id):
    return render(
        request,
        'document.html',
        {
            'eqms': eqms,
            'document': eqms.qms_documents.get_document(document_id),
        }
    )

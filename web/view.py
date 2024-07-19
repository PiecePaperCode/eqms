from django.http import HttpResponseRedirect
from django.shortcuts import render

from eqms.document import Document
from eqms.eqms import eQMS
from django import forms

from eqms.user import User, Role

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


def render_document(request, document_id, version=None, operation=None):
    if operation == "create":
        new_version_document = eqms.qms_documents.get_document(document_id)
        eqms.qms_documents.add_document(new_version_document)
    if operation == "sign":
        eqms.qms_documents.sign(
            document_id,
            User('Tom Scott', roles=[Role.QA])
        )
    if operation is not None:
        return HttpResponseRedirect(f"/document/{document_id}")
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            updated_document = Document("")
            updated_document.__dict__.update(form.cleaned_data)
            if operation:
                eqms.qms_documents.add(updated_document)
            else:
                eqms.qms_documents.update_document(document_id, updated_document)
        else:
            raise Exception(form.errors)
    form = DocumentForm(
        eqms.qms_documents.get_document(document_id, version).__dict__
    )
    return render(
        request,
        'document.html',
        {
            'eqms': eqms,
            'document': form,
            'versions': eqms.qms_documents.get_versions(document_id)
        }
    )


class DocumentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    name = forms.CharField()
    version = forms.CharField()
    author = forms.CharField()
    effective = forms.CharField()
    withdrawn = forms.CharField()
    signed_by = forms.CharField()
    withdrawn_by = forms.CharField()
    uuid = forms.CharField(widget=forms.HiddenInput)

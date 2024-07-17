from django.http import HttpResponseRedirect
from django.shortcuts import render

from eqms.document import Document
from eqms.eqms import eQMS
from django import forms

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


def render_document(request, document_id, version=None):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            updated_document = Document("123")
            updated_document.__dict__.update(form.cleaned_data)
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

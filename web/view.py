import json
import os
import pickle

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render

from eqms.document import Document
from eqms.document_store import Store


def load_store():
    store = pickle.loads(open('store.json', 'rb').read())
    return store


def save_store(store: Store):
    with open('store.json', 'wb') as f:
        f.write(pickle.dumps(store))


def index(request):
    store = load_store()
    return render(
        request,
        'index.html',
        {'documents': store.generate_overview()}
    )


def show_document(request, document_uuid: int):
    store = load_store()
    document = store.get_document(document_uuid)
    print(document.version)
    return render(request, 'show_documents.html', {'document': document})


def create_document(request):
    class DocumentForm(forms.Form):
        name = forms.CharField(label='Name', max_length=100)
        author = forms.CharField(label='Author', max_length=100)
        text = forms.CharField(label='Markdown', widget=forms.Textarea)
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            document = Document(
                name=form.cleaned_data['name'],
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                version=1
            )
            store = load_store()
            store.add_document(document)
            save_store(store)
            return HttpResponseRedirect("/")
    return render(request, "create_documents.html", {'form': DocumentForm()})

import json
import os
import pickle

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

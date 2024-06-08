from django.shortcuts import render
from eqms.eqms import eQMS

eqms = eQMS('Dunder Mifflin')


def index(request):
    eqms = eQMS('Dunder Mifflin')
    eqms.initialize_qms_project()
    return render(
        request,
        'base.html',
        {'eqms': eqms}
    )

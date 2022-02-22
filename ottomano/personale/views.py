from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import personale.importa_dati

from personale.models import Lavoratore


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def importa_Personale_abilitazioni(request):
    personale.importa_dati.importa_xlsx()
    return HttpResponse("xls importato")

def anagrafica(request):
    lavoratori = Lavoratore.objects.all()
    context = {'titolo': 'Anagrafica',
               'lavoratori': lavoratori}

    return render(request, 'personale/base.html', context)
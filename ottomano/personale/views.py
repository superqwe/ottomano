from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import personale.importa_dati

from personale.models import Lavoratore, Formazione


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# def importa_Personale_abilitazioni(request):
#     personale.importa_dati.importa_xlsx()
#     return HttpResponse("xls importato")

def anagrafica(request):
    lavoratori = Lavoratore.objects.all()
    context = {'titolo': 'Anagrafica',
               'lavoratori': lavoratori}

    return render(request, 'personale/base.html', context)


def formazione(request):
    formazione = Formazione.objects.all()
    print(formazione)
    context = {'titolo': 'Formazione',
               'formazione': formazione}

    return render(request, 'personale/formazione.html', context)

def aggiorna_documenti(request):
    formazione = Formazione.objects.all()
    print(formazione)
    context = {'titolo': 'Formazione',
               'formazione': formazione}

    return render(request, 'personale/aggiorna_documenti.html', context)

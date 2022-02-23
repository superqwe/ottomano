import os

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
# import personale.importa_dati

from personale.models import Lavoratore, Formazione

PATH_DOCUMENTI = r'C:\Users\benedetto.basile\Dropbox\Documenti_Lavoratori'


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
    # verifica se sono presenti nuovi lavoratori
    elenco_lavoratori = Lavoratore.objects.all().values_list('cognome', 'nome')
    elenco_lavoratori = [('%s %s' % lavoratore).lower() for lavoratore in elenco_lavoratori]

    dir_lavoratori = os.listdir(PATH_DOCUMENTI)
    dir_lavoratori = [lavoratore.lower() for lavoratore in dir_lavoratori]

    nuovi_lavoratori=[]
    for lavoratore in dir_lavoratori:
        if not lavoratore in elenco_lavoratori:
            if os.path.isdir(lavoratore):
                nuovi_lavoratori.append(lavoratore)
                print('\n'*3, 'Nuovo lavoratore', lavoratore, '\n'*3)
                #todo: implementare nuovo lavoratore


    ####
    # formazione = Formazione.objects.all()
    # print(formazione)

    context = {'titolo': 'Aggiorna Documenti',
               'nuovi_lavoratori': nuovi_lavoratori}

    return render(request, 'personale/aggiorna_documenti.html', context)

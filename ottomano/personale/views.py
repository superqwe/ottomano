import os

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
# import personale.importa_dati
from django.core.exceptions import ObjectDoesNotExist
from personale.models import Lavoratore, Formazione

from pprint import pprint as pp

from personale import aggiorna_documenti_util

PATH_DOCUMENTI = r'C:\Users\benedetto.basile\Dropbox\Documenti_Lavoratori'


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# def importa_Personale_abilitazioni(request):
#     personale.importa_dati.importa_xlsx()
#     return HttpResponse("xls importato")

def anagrafica(request):
    lavoratori = Lavoratore.objects.filter(in_forza=True)
    context = {'titolo': 'Anagrafica',
               'pagina_attiva_anagrafica': 'active',
               'lavoratori': lavoratori}

    return render(request, 'personale/base.html', context)


def formazione(request):
    formazione = Formazione.objects.filter(lavoratore__in_forza=True)
    # print(formazione)
    context = {'titolo': 'Formazione',
               'pagina_attiva_formazione': 'active',
               'formazione': formazione}

    return render(request, 'personale/formazione.html', context)


def aggiorna_documenti(request):
    # verifica se sono presenti nuovi lavoratori
    elenco_lavoratori = Lavoratore.objects.all().values_list('cognome', 'nome').order_by('cognome')
    elenco_lavoratori = [('%s %s' % lavoratore).lower() for lavoratore in elenco_lavoratori]

    dir_lavoratori = os.listdir(PATH_DOCUMENTI)
    dir_lavoratori = [lavoratore.lower() for lavoratore in dir_lavoratori]

    nuovi_lavoratori = []
    lista_documenti = []
    for lavoratore in dir_lavoratori:
        # print(lavoratore)

        if not lavoratore in elenco_lavoratori:

            if os.path.isdir(lavoratore):
                nuovi_lavoratori.append(lavoratore)
                print('\n' * 3, 'Nuovo lavoratore', lavoratore, '\n' * 3)
                # todo: implementare nuovo lavoratore
            else:
                continue

        # ricerca documenti
        path_attestati = os.path.join(PATH_DOCUMENTI, lavoratore, 'attestati')
        try:
            attestati = os.listdir(path_attestati)
            attestati = aggiorna_documenti_util.calcola_data_attestati(attestati)
        except FileNotFoundError:
            attestati = []

        lista_documenti.append([lavoratore, attestati])

        # salva su db
        if attestati or True:
            cognome, nome = lavoratore.split(maxsplit=1)

            try:
                formazione_ = Formazione.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)
                # print('----->', formazione_)
            except ObjectDoesNotExist:
                lavoratore = Lavoratore.objects.get(cognome__iexact=cognome, nome__iexact=nome)
                formazione_ = Formazione(lavoratore=lavoratore)

            for corso, data in attestati:
                setattr(formazione_, corso, data)

            formazione_.save()
            #
            # formazione = Formazione(lavoratore=lavoratore)
            # formazione.save()

            # for corso, data in attestati:
            #     lavoratore[corso]=corso

    # pp(lista_documenti)

    ####
    # formazione = Formazione.objects.all()
    # print(formazione)

    context = {'titolo': 'Aggiorna Documenti',
               'pagina_attiva_aggiorna_documenti': 'active',
               'lista_documenti': lista_documenti}

    return render(request, 'personale/aggiorna_documenti.html', context)

import datetime
import os.path
import warnings
from pprint import pprint as pp

from django.http import HttpResponse
from django.shortcuts import render
from mezzi.models import Mezzo

from mezzi import views_util

# import personale.importa_dati

pp('')
PATH_DOCUMENTI = r'C:\Users\benedetto.basile\Dropbox\Documenti_Mezzi\New Folder'


def index(request):
    return HttpResponse("Hello, world. You're at the mezzi index.")


def elenco(request):
    mezzi = Mezzo.objects.filter(in_forza=True)
    context = {'titolo': 'Elenco Mezzi',
               'pagina_attiva_elenco': 'active',
               'mezzi': mezzi}

    return render(request, 'mezzi/base.html', context)


def scadenziario(request):
    return HttpResponse("Hello, world. You're at the mezzi index.")


def aggiorna_stato(request):
    return HttpResponse("Hello, world. You're at the mezzi index.")


def aggiorna_documenti(request):
    elenco_mezzi = Mezzo.objects.all()

    for mezzo in elenco_mezzi:
        print('\n', mezzo.nome())
        path_mezzo = os.path.join(PATH_DOCUMENTI, mezzo.nome())

        documenti = os.listdir(path_mezzo)

        for documento in documenti:
            doc = os.path.splitext(documento)[0].split()

            match doc[0]:
                case 'assicurazione':
                    data = views_util.str2datetime(doc[1])
                    mezzo.assicurazione = data
                case 'immatricolazione':
                    data = views_util.str2datetime(doc[1])
                    mezzo.immatricolazione = data

                    if mezzo.inail == None:
                        data_inail = views_util.aggiungi_anni(data)
                        mezzo.inail = data_inail

                case 'libretto':
                    match len(doc):
                        case 2:
                            data = views_util.str2datetime(doc[1])
                            mezzo.revisione = data
                            mezzo.libretto = True
                        case 1:
                            mezzo.libretto = True
                        case _:
                            warnings.warn('Nome file errato - %s' % documento)
                case _:
                    print(doc)

        mezzo.save()

    return HttpResponse("Hello, world. You're at the aggiorna mezzi index.")

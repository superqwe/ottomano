import datetime
import os.path
import warnings
from pprint import pprint as pp

from django.http import HttpResponse
from django.shortcuts import render
from mezzi.models import Mezzo

from mezzi import views_util

pp('')
PATH_DOCUMENTI = r'C:\Users\L. MASI\Documents\Documenti_Mezzi'


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

    elenco_documenti_mezzi = []
    for mezzo in elenco_mezzi:
        # print('\n', mezzo.nome())
        path_mezzo = os.path.join(PATH_DOCUMENTI, mezzo.nome())

        documenti = os.listdir(path_mezzo)

        documenti_mezzo_ok = []
        documenti_mezzo_errore = []
        for documento in documenti:
            documenti_mezzo_ok.append(os.path.splitext(documento)[0])
            doc = os.path.splitext(documento)[0].split()

            match doc[0]:
                case 'altro':
                    documenti_mezzo_errore.append((documenti_mezzo_ok.pop()))

                case 'assicurazione':
                    data = views_util.str2datetime(doc[1])
                    mezzo.assicurazione = data

                case 'ce':
                    mezzo.ce = True

                case 'ce_accessori':
                    mezzo.ce_accessori = True

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
                            documenti_mezzo_errore.append((documenti_mezzo_ok.pop()))
                            warnings.warn('Nome file errato - %s' % documento)

                case 'libretto_inail':
                    mezzo.libretto_inail = True

                case 'manuale':
                    mezzo.manuale = True

                case 'verifica_periodica':
                    data = views_util.str2datetime(doc[1])
                    data_scadenza_verifica = views_util.aggiungi_anni(data)
                    mezzo.inail = data_scadenza_verifica

                case _:
                    documenti_mezzo_errore.append((documenti_mezzo_ok.pop()))
                    warnings.warn('Nome documento non processato - %s (%s)' % (mezzo, documento))

        mezzo.save()
        elenco_documenti_mezzi.append((mezzo, documenti_mezzo_ok, documenti_mezzo_errore))

    context = {'titolo': 'Documenti Mezzi Aggiornati',
               'pagina_attiva_aggiorna_documenti': 'active',
               'mezzi': elenco_documenti_mezzi}

    return render(request, 'mezzi/aggiorna_documenti.html', context)

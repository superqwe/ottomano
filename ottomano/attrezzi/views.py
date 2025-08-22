import os
import warnings

from attrezzi.models import Attrezzo
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

if settings.NOME_COMPUTER.lower() == 'srvdc1':
    PATH_DOCUMENTI = r'D:\Gestionale\Documenti_Attrezzi'
else:
    PATH_DOCUMENTI = r'C:\Users\L. MASI\Documents\Documenti_Attrezzi'


def index(request):
    return HttpResponse("Hello, world. You're at the attrezzi index.")


def elenco(request):
    attrezzi = Attrezzo.objects.all()
    context = {'titolo': 'Elenco Attrezzi',
               'sezione_attrezzi_attiva': 'active',
               'pagina_attiva_elenco': 'active',
               'attrezzi': attrezzi}

    return render(request, 'attrezzi/elenco.html', context)


def aggiorna_documenti(request):
    elenco_attrezzi = Attrezzo.objects.all()

    elenco_documenti_attrezzi = []

    for attrezzo in elenco_attrezzi:
        path_attrezzo = os.path.join(PATH_DOCUMENTI, attrezzo.tipologia.nome, attrezzo.nome())

        try:
            documenti = os.listdir(path_attrezzo)

            documenti_attrezzo_ok = []
            documenti_attrezzo_errore = []

            for documento in documenti:
                documenti_attrezzo_ok.append(os.path.splitext(documento)[0])
                doc = os.path.splitext(documento)[0].split()

                match doc[0]:

                    case 'ce':
                        attrezzo.ce = True

                    case 'manuale':
                        attrezzo.manuale = True

                    case _:
                        documenti_attrezzo_errore.append((documenti_attrezzo_ok.pop()))
                        warnings.warn('Nome documento non processato - %s (%s)' % (attrezzo, documento))

        except FileNotFoundError:
            documenti = None
            warnings.warn(f'Percorso non trovato - {path_attrezzo}')

        attrezzo.save()
        elenco_documenti_attrezzi.append((attrezzo, documenti_attrezzo_ok, documenti_attrezzo_errore))

    context = {'titolo': 'Documenti Mezzi Aggiornati',
               'sezione_attrezzi_attiva': 'active',
               'pagina_attiva_aggiorna_documenti': 'active',
               'attrezzi': elenco_documenti_attrezzi}

    return render(request, 'attrezzi/aggiorna_documenti.html', context)

import csv
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from sgi.models import Formazione

from pprint import pprint as pp

FORMAZIONE_ANNO = 2023


def index(request):
    """"importa csv"""
    MESE = {'Gennaio': '01',
            'Febbraio': '02',
            'Marzo': '03',
            'Aprile': '04',
            'Maggio': '05',
            'Giugno': '06',
            'Luglio': '07',
            'Agosto': '08',
            'Settembre': '09',
            'Ottobre': '10',
            'Novembre': '11',
            'Dicembre': '12',
            }
    with open(r'C:\Users\benedetto.basile\Dropbox\SGI\Formazione\importare.csv') as file:
        reader = csv.reader(file, dialect='excel', delimiter=';')
        next(reader)  # Advance past the header

        for row in reader:
            mese, corso, data, argomento, docente, ore, persone = row[:-1]

            mese = MESE[mese]
            data = datetime.strptime(data, '%d/%m/%Y').date()
            corso = corso if corso else None

            print(mese, corso, data, argomento, docente, ore, persone)

            formazione = Formazione(mese=mese, corso=corso, data=data, argomento=argomento, docente=docente, ore=ore,
                                    persone=persone
                                    )
            # formazione.save()

    return HttpResponse("Hello, world. You're at the personale index.")


def formazione(request, anno=FORMAZIONE_ANNO):
    formazione_ = Formazione.objects.filter(data__year=anno)

    context = {'titolo': 'Programma di informazione, formazione, addestramento',
               'pagina_attiva_formazione': 'active',
               'formazione': formazione_,
               }

    pagina_attiva_formazione_2023 = pagina_attiva_formazione_2022 = ''

    match anno:
        case 2023:
            pagina_attiva_formazione_2023 = 'active'
        case 2022:
            pagina_attiva_formazione_2022 = 'active'

    context['pagina_attiva_formazione_2023'] = pagina_attiva_formazione_2023
    context['pagina_attiva_formazione_2022'] = pagina_attiva_formazione_2022

    return render(request, 'sgi/formazione.html', context)
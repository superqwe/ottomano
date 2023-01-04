import csv
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from sgi.models import Formazione

import pandas as pd


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


def formazione(request):
    formazione_ = Formazione.objects.all()

    context = {'titolo': 'Programma di informazione, formazione, addestramento',
               'pagina_attiva_formazione': 'active',
               'formazione': formazione_,
    #            'conteggio_rg': conteggio_rg(formazione_)
               }

    # return HttpResponse("Hello SGI, world. You're at the personale index.")
    return render(request, 'sgi/formazione.html', context)

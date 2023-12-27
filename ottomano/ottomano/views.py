from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import pandas as pd

from personale.models import Lavoratore

from pprint import pprint as pp


def index(request):
    return HttpResponseRedirect("/personale/formazione")


# def index(request):
#     importa_dati_anagrafica()
#     return HttpResponse("Hello, world. You're at the personale index 8080.")


def importa_dati_anagrafica():
    PATH_XLSX = r'C:\Users\L. MASI\Documents\Programmi\ore\Elenco_personale_2023_agg_31_08.xls'

    df = pd.read_excel(PATH_XLSX, sheet_name='ELENCO 2022', skiprows=2, na_values='')
    df.drop(columns='Unnamed: 0', inplace=True)

    print(df.columns)

    for index, row in df.iterrows():
        cf = row.CodiceFiscale
        lavoratore = Lavoratore.objects.get(cf=cf)
        print(lavoratore)

        lavoratore.matricola = row.Matricola
        lavoratore.indirizzo = row.Indirizzo
        lavoratore.citta = row.Comune
        lavoratore.provincia = row.Prov
        lavoratore.cap = row.CAP
        lavoratore.data_nascita = row.DataNascita
        lavoratore.luogo_nascita = row.LuogoNascita
        lavoratore.email = row.IndirizzoMail

        # lavoratore.save()

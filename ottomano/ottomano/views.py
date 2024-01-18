from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import pandas as pd

from personale.models import Lavoratore
from sgi.models import RilevatoreH2S

from pprint import pprint as pp


def index(request):
    return HttpResponseRedirect("/personale/formazione")


# def index(request):
#     importa_rilevatori()
#     return HttpResponse("Hello, world. You're at the personale index 8080 importa_rilevatori.")


def importa_rilevatori():
    PATH_XLSX = r'C:\Users\L. MASI\Documents\Programmi\ottomano\ottomano\240124 Scadenzario DPI.xlsx'
    df = pd.read_excel(PATH_XLSX, sheet_name='Foglio2', skiprows=0, na_values=None)
    # print(df.columns)

    for index, row in df.iterrows():
        # print('\n', row.Cognome.title())
        rilevatore = RilevatoreH2S()
        try:
            lavoratore = Lavoratore.objects.get(cognome=row.Cognome.strip().title(), nome=row.Nome.strip().title())
            rilevatore.uso = 'l'
            rilevatore.lavoratore = lavoratore
        except:
            rilevatore.uso = 'd'

        rilevatore.matricola = row.Matricola
        rilevatore.data_scadenza = row.Scadenza

        match row.Tipo:
            case 'Drager':
                rilevatore.marca = 'dr'
            case 'Honeywell':
                rilevatore.marca = 'hw'
            case 'MSA':
                rilevatore.marca = 'ms'

        # rilevatore.save()



def importa_dati_anagrafica2():
    PATH_XLSX = r'C:\Users\L. MASI\Documents\Programmi\ottomano\ottomano\231227_2 personale_lavoratore  - paola.xlsx'
    df = pd.read_excel(PATH_XLSX, sheet_name='personale_lavoratore', skiprows=0, na_values='')
    print(df.columns)

    for index, row in df.iterrows():
        lavoratore = Lavoratore.objects.get(id=row.id)
        print(lavoratore)

        # lavoratore.cf = row['CODICE FISCALE']
        # lavoratore.sesso = row['SESSO']
        #
        # if pd.notna(row['DATA DI NASCITA']):
        #     lavoratore.data_nascita = row['DATA DI NASCITA']
        #
        # lavoratore.luogo_nascita = row['LUOGO NASCITA']
        #
        # if pd.notna(row['PROVINCIA DI NASCITA']):
        #     lavoratore.provincia_nascita = row['PROVINCIA DI NASCITA']
        # else:
        #     lavoratore.provincia_nascita = None
        #
        # lavoratore.indirizzo = row['RESIDENZA']
        # if not pd.isna(row['CAP']):
        #     lavoratore.cap = row['CAP']
        #
        # lavoratore.citta = row["CITTA'"]
        # lavoratore.provincia = row['PROVINCIA']
        #
        # if not pd.isna(row['CELLULARE']):
        #     lavoratore.cellulare = row['CELLULARE']
        #
        # lavoratore.email = row['E MAIL']
        # lavoratore.tipo_contratto = row['CONTRATTO']
        #
        # if pd.notna(row['DATA ASSUNZIONE']):
        #     lavoratore.data_inizio = row['DATA ASSUNZIONE']
        #
        if pd.notna(row['SCADENZA CONTRATTO']):
            lavoratore.data_fine = row['SCADENZA CONTRATTO']
        else:
            lavoratore.data_fine = None
        #
        # if pd.notna(row['LIVELLO']):
        #     lavoratore.livello = int(row['LIVELLO'])
        # lavoratore.qualifica = row['QUALIFICA ATTUALE']
        # lavoratore.assunzione = row['QUALIFICA ASSUNZIONE']
        # lavoratore.busta_paga = row['MANSIONE_BUSTA_PAGA']

        # lavoratore.save()


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

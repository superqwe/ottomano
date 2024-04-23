from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import pandas as pd

from personale.models import Lavoratore
from sgi.models import DPI_Anticaduta2

from pprint import pprint as pp


def index(request):
    return HttpResponseRedirect("/personale/formazione")


# def index(request):
#     importa_imbracature()
#     return HttpResponse("Hello, world. You're at the importa_funi_catene.")


def importa_imbracature():
    PATH_XLSX = r'C:\Users\L. MASI\Documents\Programmi\ottomano\ottomano\240417 Cinture sicurezza.xlsx'
    df = pd.read_excel(PATH_XLSX, sheet_name='2023 Nuovo', skiprows=0, na_values=None)

    for index, row in df.iterrows():
        print(row.nominativo)

        if not pd.isna(row.matrIM):
            print('im', row.nominativo, row.matrIM)
            dpi = DPI_Anticaduta2()
            dpi.tipologia = 'im'
            dpi.stato = 'c'

            if not pd.isna(row.servizioIM):
                dpi.messa_in_servizio = row.servizioIM

            dpi.marca = row.marcaIM
            dpi.modello = row.tipoIM
            dpi.fabbricazione = row.fabbrIM
            dpi.matricola = row.matrIM

            dpi.save()

        if not pd.isna(row.matrC1):
            print('c1', row.nominativo, row.matrC1)
            dpi = DPI_Anticaduta2()
            dpi.tipologia = 'c1'
            dpi.stato = 'c'

            if not pd.isna(row.servizioC1):
                dpi.messa_in_servizio = row.servizioC1

            dpi.marca = row.marcaC1
            dpi.modello = row.tipoC1
            dpi.fabbricazione = row.fabbrC1
            dpi.matricola = row.matrC1

            dpi.save()

        if not pd.isna(row.matrC2):
            print('c2', row.nominativo, row.matrC2)
            dpi = DPI_Anticaduta2()
            dpi.tipologia = 'c2'
            dpi.stato = 'c'

            if not pd.isna(row.servizioC2):
                dpi.messa_in_servizio = row.servizioC2

            dpi.marca = row.marcaC2
            dpi.modello = row.tipoC2
            dpi.fabbricazione = row.fabbrC2
            dpi.matricola = row.matrC2


            dpi.save()

        print()


def importa_funi_catene():
    PATH_XLSX = r'C:\Users\L. MASI\Documents\Programmi\ottomano\ottomano\240415 ACCESSORI DI SOLLEVAMENTO MOD ACS t2 r10 bozza.xlsm'
    df = pd.read_excel(PATH_XLSX, sheet_name='ACCESSORI DI SOLLEVAMENTO', skiprows=0, na_values=None)

    for index, row in df.iterrows():
        print(row.codice)

        accessorio = AccessoriSollevamento()

        accessorio.tipo = row.codice.split()[0].lower()

        if not pd.isna(row.marca):
            accessorio.marca = row.marca

        if not pd.isna(row.anno):
            accessorio.anno = int(row.anno)

        accessorio.codice = row.codice

        if not pd.isna(row.diametro):
            accessorio.diametro = row.diametro

        if not pd.isna(row.colore):
            accessorio.colore = row.colore

        if not pd.isna(row.lunghezza):
            accessorio.lunghezza = row.lunghezza

        if accessorio.tipo == 'f':
            match accessorio.colore:
                case 'a':
                    accessorio.portata = 10
                case 'b':
                    accessorio.portata = 8
                case 'g':
                    accessorio.portata = 3
                case 'gr':
                    accessorio.portata = 4
                case 'm':
                    accessorio.portata = 6
                case 'v':
                    accessorio.portata = 2
                case _:
                    accessorio.portata = row.portata

        if not pd.isna(row.terminali):
            accessorio.terminali = row.terminali

        accessorio.reparto = row.reparto

        if row.leggero == 'L':
            accessorio.usura_leggera = True

        if row.medio == 'M':
            accessorio.usura_media = True

        if row.sostituzione in ('G', 'S'):
            accessorio.usura_grave = True
            accessorio.usura_sostituzione = True
            accessorio.conforme = False
            accessorio.in_uso = False

        if not pd.isna(row.servizio):
            accessorio.data_messa_in_servizio = row.servizio

        if not pd.isna(row.dismissione):
            accessorio.data_dismissione = row.dismissione

        if not pd.isna(row.note):
            accessorio.note = row.note

        # accessorio.save()


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

import pandas as pd

from personale.models import Lavoratore

PATH_XLSX = r'C:\Users\benedetto.basile\Desktop\FORNARO\Programmi\ottomano\jupyter\2019REG_Personale_abilitazioni.xlsx'


def importa_xlsx():
    df = pd.read_excel(PATH_XLSX, sheet_name='ANAGRAFICA ', skiprows=6, na_values='')
    df.drop(columns='#', inplace=True)
    df = df.where(pd.notnull(df), None)
    df.replace('______', None, inplace=True)
    df.replace('-----', None, inplace=True)

    for index, row in df.iterrows():
        # print(row['Cognome '], row['Nome'],  '\n' * 10, )

        if not pd.isna(row['matr']):
            matricola = row['matr']
        else:
            matricola = None

        if not pd.isna(row['cellulare']):
            cellulare = int(str(row['cellulare']).replace('.','').replace(' ', ''))
        else:
            cellulare = None

        if not pd.isna(row['fine lavoro']):
           fine_lavoro =  row['fine lavoro']
        else:
           fine_lavoro =  None

        lavoratore = Lavoratore(
            matricola=matricola,
            cognome=row['Cognome '].strip().title(),
            nome=row['Nome'].strip().title(),
            cf=row['Codice fiscale'],
            sesso=row['Sesso'],
            data_nascita=row['Data di nascita'],
            luogo_nascita=row['Luogo di nascita'],
            provincia_nascita=row['Provincia di nascita'],
            indirizzo=row['Indirizzo'],
            cap=row['CAP'],
            citta=row['Città'],
            provincia=row['Provincia'],
            cellulare=cellulare,
            data_inizio=row['data assunzione'],
            tipo_contratto=row['Contratto'],
            data_fine=fine_lavoro,
            livello=row[' liv.'],
            qualifica=row['qualifica '],
            assunzione=row['assunzione'],
            busta_paga=row['busta paga'],
            mansione=row['Mansione'],
            attivita_svolta=row['Attività svolta'],
            mansione_1=row['mansione 1'],
            mansione_2=row['mansione 2'],
            mansione_3=row['mansione 3'],
            reparto=row['Reparto']
        )
        #     print(row)
        print(row['Cognome '], row['Nome'])

        lavoratore.save()

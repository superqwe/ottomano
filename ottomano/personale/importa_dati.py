import pandas as pd

PATH_XLSX = r'C:\Users\benedetto.basile\Desktop\FORNARO\Programmi\ottomano\jupyter\2019REG_Personale_abilitazioni.xlsx'


def importa_xlsx():
    df = pd.read_excel(PATH_XLSX, sheet_name='ANAGRAFICA ', skiprows=6, na_values='')
    df.drop(columns='#', inplace=True)

    for index, row in df.iterrows():
        #     print(row)
        print(row['Cognome '], row['Nome'], row['Codice fiscale'])

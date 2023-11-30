import configparser
import glob
import math
import os
import pathlib
import shutil
from itertools import islice
from pprint import pprint as pp
import zipfile
import datetime

N_COLONNE = 6
CFG = 'estrai.cfg'
PATH_BASE = pathlib.Path(r'C:\Users\L. MASI\Documents\Documenti_Lavoratori')
PATH_ESTRAI = pathlib.Path(r'C:\Users\L. MASI\Documents\Documenti_Estratti')


def chunk(arr_range, arr_size):
    arr_range = iter(arr_range)
    return iter(lambda: tuple(islice(arr_range, arr_size)), ())


def dividi_elenco_lavoratori(lavoratori, n_colonne=N_COLONNE):
    nlavoratori = len(lavoratori)
    gruppi = chunk(lavoratori, math.ceil(nlavoratori / n_colonne))
    return gruppi, n_colonne


class Estrai_Dati():
    def __int__(self):
        print('ciaoo ' * 20)

    def salva_lavoratori(self, lavoratori):
        config = configparser.ConfigParser()
        config.read(CFG)

        lavoratori = [lavoratore.id for lavoratore in lavoratori]
        config['DEFAULT'] = {'lavoratori': lavoratori}

        with open(CFG, 'w') as cfg:
            config.write(cfg)

    def estrai(self, elenco_lavoratori, elenco_formazione, elenco_nomine):

        try:
            shutil.rmtree(PATH_ESTRAI)
        except (PermissionError, FileNotFoundError):
            pass

        tabella = []
        for lavoratore in elenco_lavoratori:
            cognome, nome = lavoratore.lavoratore.cognome, lavoratore.lavoratore.nome
            rigo = [(cognome, nome), ]

            # todo: campo *_ck non funzionante
            attestati = [(getattr(lavoratore, formazione), getattr(lavoratore, '{}_ck'.format(formazione))) for
                         formazione in elenco_formazione]
            rigo.append(attestati)

            nomine = [getattr(lavoratore, nomina) for nomina in elenco_nomine]
            rigo.append(nomine)

            tabella.append(rigo)

            # salva documenti
            nominativo = f'{cognome} {nome}'
            path_lavoratore = PATH_BASE / nominativo
            path_lavoratore_attestati = path_lavoratore / 'attestati'
            path_lavoratore_nomine = path_lavoratore / 'nomine'

            pathlib.Path(PATH_ESTRAI).mkdir(parents=True, exist_ok=True)

            # todo: gestire gli errori
            errori = []
            for nome_attestato, (data_attestato, dummy) in zip(elenco_formazione, attestati):
                if data_attestato:
                    nome_originale = '{} {}.pdf'.format(nome_attestato,
                                                        getattr(lavoratore,
                                                                '{}_dc'.format(nome_attestato)).strftime('%d%m%y'))
                    nome_destinazione = '{} {}.pdf'.format(nominativo, nome_attestato)

                    path_originale = path_lavoratore_attestati / nome_originale
                    path_destinazione = PATH_ESTRAI / nome_destinazione

                    shutil.copy(path_originale, path_destinazione)

            for nome_nomina, nomina_esistente in zip(elenco_nomine, nomine):
                if nomina_esistente:
                    nome_originale = '{} {}.pdf'.format(nome_nomina,
                                                        getattr(lavoratore, nome_nomina).strftime('%d%m%y'))
                    nome_destinazione = '{} {}.pdf'.format(nominativo, nome_nomina)

                    path_originale = path_lavoratore_nomine / nome_originale
                    path_destinazione = PATH_ESTRAI / nome_destinazione
                    print(path_originale, path_destinazione)

                    shutil.copy(path_originale, path_destinazione)

        # pp(tabella)

        # zippa i file estratti
        path_iniziale = pathlib.Path.cwd()
        os.chdir(PATH_ESTRAI)

        file_zip = '{}.zip'.format(datetime.datetime.now().strftime('%y%m%d%H%M%S'))
        with zipfile.ZipFile(file_zip, 'w') as zip_pdf:
            lfile = glob.glob('*.pdf')
            for nfile in lfile:
                zip_pdf.write(nfile)

        os.chdir(path_iniziale)

        return tabella

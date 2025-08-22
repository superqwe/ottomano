import configparser
import datetime
import glob
import math
import os
import pathlib
import shutil
import zipfile
from itertools import islice

from django.conf import settings
from icecream import ic

from personale.models import Idoneita
from sgi.models import DPI2

N_COLONNE = 6
CFG = 'estrai.cfg'
if settings.NOME_COMPUTER.lower() == 'srvdc1':
    PATH_BASE = pathlib.Path(r'D:\Gestionale\Documenti_Lavoratori')
    PATH_ESTRAI = pathlib.Path(r'D:\Gestionale\Documenti_Estratti')
else:
    PATH_BASE = pathlib.Path(r'C:\Users\L. MASI\Documents\Documenti_Lavoratori')
    PATH_ESTRAI = pathlib.Path(r'C:\Users\L. MASI\Documents\Documenti_Estratti')


def chunk(arr_range, arr_size):
    arr_range = iter(arr_range)
    return iter(lambda: tuple(islice(arr_range, arr_size)), ())


def dividi_elenco_lavoratori(lavoratori, n_colonne=N_COLONNE):
    nlavoratori = len(lavoratori)
    gruppi = chunk(lavoratori, math.ceil(nlavoratori / n_colonne))
    return gruppi, n_colonne


class Estrai_Dati:
    def __int__(self):
        print('ciaoo ' * 20)

    @staticmethod
    def salva_lavoratori(lavoratori):
        config = configparser.ConfigParser()
        config.read(CFG)

        lavoratori = [lavoratore.id for lavoratore in lavoratori]
        config['DEFAULT'] = {'lavoratori': lavoratori}

        with open(CFG, 'w') as cfg:
            config.write(cfg)

    @staticmethod
    def estrai(elenco_lavoratori, elenco_formazione, elenco_nomine, elenco_documenti):
        try:
            shutil.rmtree(PATH_ESTRAI)
        except (PermissionError, FileNotFoundError):
            pass

        tabella = []
        file_non_trovati = []
        for lavoratore in elenco_lavoratori:
            # ic(lavoratore)
            cognome, nome = lavoratore.lavoratore.cognome, lavoratore.lavoratore.nome
            rigo = [(cognome, nome), ]

            # todo: campo *_ck non funzionante
            attestati = [(getattr(lavoratore, formazione), getattr(lavoratore, '{}_ck'.format(formazione))) for
                         formazione in elenco_formazione]
            rigo.append(attestati)

            nomine = [getattr(lavoratore, nomina) for nomina in elenco_nomine]
            rigo.append(nomine)

            documenti = []
            if 'unilav' in elenco_documenti:
                tipo_contratto = lavoratore.lavoratore.tipo_contratto
                if tipo_contratto in ('T.I.', 'T.I. - P. TIME'):
                    nome_documento = 'Indeterminato'
                elif lavoratore.tipo_contratto == 'T.D.':
                    nome_documento = lavoratore.lavoratore.data_fine
                else:
                    print(f'*** {lavoratore} con contratto da gestire per estrazione - {tipo_contratto} -  ***')
                    nome_documento = None

                documenti.append((nome_documento, None, 'unilav'))

            if 'idoneita' in elenco_documenti:
                idoneita_ = Idoneita.objects.filter(lavoratore=lavoratore.lavoratore).first()
                idoneita = idoneita_.idoneita
                idoneita_ck = idoneita_.idoneita_ck

                documenti.append((idoneita, idoneita_ck, 'idoneita'))

            if 'consegna_dpi' in elenco_documenti:
                consegna_dpi = DPI2.objects.filter(lavoratore=lavoratore.lavoratore).first()
                consegna = consegna_dpi.consegna
                consegna_ck = consegna_dpi.ck_consegna

                documenti.append((consegna, consegna_ck, 'consegna_dpi'))

            rigo.append(documenti)

            # ic(rigo)

            tabella.append(rigo)

            # salva documenti
            nominativo = f'{cognome} {nome}'
            path_lavoratore = PATH_BASE / nominativo
            path_lavoratore_attestati = path_lavoratore / 'attestati'
            path_lavoratore_nomine = path_lavoratore / 'nomine'

            pathlib.Path(PATH_ESTRAI).mkdir(parents=True, exist_ok=True)

            for nome_attestato, (data_attestato, dummy) in zip(elenco_formazione, attestati):
                if data_attestato:
                    nome_originale = '{} {}.pdf'.format(nome_attestato,
                                                        getattr(lavoratore,
                                                                '{}_dc'.format(nome_attestato)).strftime('%d%m%y'))
                    nome_destinazione = '{} {}.pdf'.format(nominativo, nome_attestato)

                    path_originale = path_lavoratore_attestati / nome_originale
                    path_destinazione = PATH_ESTRAI / nome_destinazione

                    try:
                        shutil.copy(path_originale, path_destinazione)
                    except FileNotFoundError:
                        file_non_trovati.append(path_originale)

            for nome_nomina, nomina_esistente in zip(elenco_nomine, nomine):
                if nomina_esistente:
                    nome_originale = '{} {}.pdf'.format(nome_nomina,
                                                        getattr(lavoratore, nome_nomina).strftime('%d%m%y'))
                    nome_destinazione = '{} {}.pdf'.format(nominativo, nome_nomina)

                    path_originale = path_lavoratore_nomine / nome_originale
                    path_destinazione = PATH_ESTRAI / nome_destinazione

                    try:
                        shutil.copy(path_originale, path_destinazione)
                    except FileNotFoundError:
                        file_non_trovati.append(path_originale)


            for nome_documento, (documento_esistente, _, __) in zip(elenco_documenti, documenti):
                if documento_esistente:

                    if nome_documento == 'unilav':
                        if documento_esistente == 'Indeterminato':
                            nome_originale = 'unilav ind.pdf'
                        else:
                            nome_originale = f'unilav {documento_esistente.strftime("%d%m%y")}.pdf'

                    elif nome_documento == 'idoneita':
                        nome_originale = f'idoneità {documento_esistente.strftime("%d%m%y")}.pdf'

                    elif nome_documento == 'consegna_dpi':
                        nome_originale = f'consegna_dpi {documento_esistente.strftime("%d%m%y")}.pdf'

                    nome_destinazione = f'{nominativo} {nome_documento}.pdf'

                    path_originale = path_lavoratore / nome_originale
                    path_destinazione = PATH_ESTRAI / nome_destinazione

                    try:
                        shutil.copy(path_originale, path_destinazione)
                    except FileNotFoundError:
                        file_non_trovati.append(path_originale)

        # ic(tabella)

        # zippa i file estratti
        path_iniziale = pathlib.Path.cwd()
        os.chdir(PATH_ESTRAI)

        file_zip = '{}.zip'.format(datetime.datetime.now().strftime('%y%m%d%H%M%S'))
        with zipfile.ZipFile(file_zip, 'w') as zip_pdf:
            lfile = glob.glob('*.pdf')
            for nfile in lfile:
                zip_pdf.write(nfile)

        os.chdir(path_iniziale)

        return tabella, file_zip, file_non_trovati

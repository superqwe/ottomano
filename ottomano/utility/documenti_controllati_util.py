import datetime
from pathlib import Path

from attrezzi.models import Attrezzo
from django.conf import settings
from icecream import ic
from mezzi.models import Mezzo
from personale.models import Lavoratore, Formazione, Idoneita
from sgi.models import DPI2
import logging

if settings.NOME_COMPUTER.lower() == 'srvdc1':
    PATH_DOCUMENTI_LAVORATORI = Path(r'D:\Gestionale\Documenti_Lavoratori')
    PATH_DOCUMENTI_MEZZI = Path(r'D:\Gestionale\Documenti_Mezzi')
    PATH_DOCUMENTI_ATTREZZI = Path(r'D:\Gestionale\Documenti_Attrezzi')
else:
    PATH_DOCUMENTI_LAVORATORI = Path(r'C:\Users\L. MASI\Documents\Documenti_Lavoratori')
    PATH_DOCUMENTI_MEZZI = Path(r'C:\Users\L. MASI\Documents\Documenti_Mezzi')
    PATH_DOCUMENTI_ATTREZZI = Path(r'C:\Users\L. MASI\Documents\Documenti_Attrezzi')


def verifica_documenti(documenti):
    return [doc for doc in sorted(documenti) if not doc.exists()]


def crea_path_documento(base_path, *parts):
    return base_path.joinpath(*parts)


def get_documenti_personale():
    tipi_formazione = ('dirigente', 'preposto', 'primo_soccorso', 'antincendio', 'art37', 'spazi_confinati',
                       'ponteggiatore', 'imbracatore', 'mmc', 'ept', 'dumper', 'rullo', 'autogru', 'gru_autocarro',
                       'carrello', 'sollevatore', 'ple', 'rls', 'aspp')
    tipi_nomine = ('nomina_preposto', 'nomina_preposto_subappalti', 'nomina_preposto_imbracatore',
                   'nomina_antincendio', 'nomina_primo_soccorso', 'nomina_aspp')

    documenti = []

    for formazione in Formazione.objects.filter(lavoratore__in_forza=True):
        lavoratore = formazione.lavoratore

        for tipo in tipi_formazione:
            data = getattr(formazione, f'{tipo}_dc')
            if data:
                nome_file = f'{tipo} {data.strftime("%d%m%y")}.pdf'
                documenti.append(
                    crea_path_documento(PATH_DOCUMENTI_LAVORATORI, f'{lavoratore}', 'attestati', nome_file))

        for tipo in tipi_nomine:
            data = getattr(formazione, tipo)
            if data:
                nome_file = f'{tipo} {data.strftime("%d%m%y")}.pdf'
                documenti.append(crea_path_documento(PATH_DOCUMENTI_LAVORATORI, f'{lavoratore}', 'nomine', nome_file))

        tipo_contratto = lavoratore.tipo_contratto
        if tipo_contratto in ('T.I.', 'T.I. - P. TIME'):
            nome_file = 'unilav ind.pdf'
        elif tipo_contratto == 'T.D.':
            nome_file = f'unilav {lavoratore.data_fine}.pdf'
        else:
            ic(f'{lavoratore} ha un contratto non gestito')
            nome_file = None

        if nome_file:
            documenti.append(crea_path_documento(PATH_DOCUMENTI_LAVORATORI, f'{lavoratore}', nome_file))

    for idoneita in Idoneita.objects.filter(lavoratore__in_forza=True):
        data = getattr(idoneita, 'idoneita')
        if data:
            nome_file = f'idoneità {data.strftime("%d%m%y")}.pdf'
            documenti.append(crea_path_documento(PATH_DOCUMENTI_LAVORATORI, f'{idoneita.lavoratore}', nome_file))

    for consegna in DPI2.objects.filter(lavoratore__in_forza=True):
        data = getattr(consegna, 'consegna')
        if data:
            nome_file = f'consegna_dpi {data.strftime("%d%m%y")}.pdf'
            documenti.append(crea_path_documento(PATH_DOCUMENTI_LAVORATORI, f'{consegna.lavoratore}', nome_file))

    return documenti


def get_documenti_mezzi():
    documenti = []
    campi = ('ce', 'ce_accessori', 'assicurazione', 'libretto', 'immatricolazione',
             'libretto_inail', 'inail', 'manuale')

    for mezzo in Mezzo.objects.filter(in_forza=True):
        for campo in campi:
            dato = getattr(mezzo, campo)
            if not dato:
                continue

            match campo:
                case 'ce' | 'ce_accessori' | 'libretto_inail' | 'manuale':
                    nome_file = f'{campo}.pdf'
                case 'assicurazione' | 'immatricolazione':
                    nome_file = f'{campo} {dato.strftime("%d%m%y")}.pdf'
                case 'libretto':
                    revisione = getattr(mezzo, 'revisione')
                    nome_file = f'libretto {revisione.strftime("%d%m%y")}.pdf' if revisione else 'libretto.pdf'
                case 'inail':
                    data = datetime.date(dato.year - 1, dato.month, dato.day)
                    nome_file = f'verifica_periodica {data.strftime("%d%m%y")}.pdf'
                case _:
                    continue

            documenti.append(crea_path_documento(PATH_DOCUMENTI_MEZZI, f'{mezzo}', nome_file))

    return documenti


def get_documenti_attrezzi():
    documenti = []
    for attrezzo in Attrezzo.objects.all():
        for campo in ('ce', 'manuale'):
            dato = getattr(attrezzo, campo)
            if dato:
                nome_file = f'{campo}.pdf'
                documenti.append(
                    crea_path_documento(PATH_DOCUMENTI_ATTREZZI, f'{attrezzo.tipologia}', f'{attrezzo}', nome_file))
    return documenti

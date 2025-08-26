import datetime
from pathlib import Path

from attrezzi.models import Attrezzo
from django.conf import settings
from django.shortcuts import render
from icecream import ic
from mezzi.models import Mezzo
from personale.models import Lavoratore, Formazione, Idoneita
from sgi.models import DPI2
from utility import estrai_dati_util

if settings.NOME_COMPUTER.lower() == 'srvdc1':
    PATH_DOCUMENTI_LAVORATORI = Path(r'D:\Gestionale\Documenti_Lavoratori')
    PATH_DOCUMENTI_MEZZI = Path(r'D:\Gestionale\Documenti_Mezzi')
    PATH_DOCUMENTI_ATTREZZI = Path(r'D:\Gestionale\Documenti_Attrezzi')
else:
    PATH_DOCUMENTI_LAVORATORI = Path(r'C:\Users\L. MASI\Documents\Documenti_Lavoratori')
    PATH_DOCUMENTI_MEZZI = Path(r'C:\Users\L. MASI\Documents\Documenti_Mezzi')
    PATH_DOCUMENTI_ATTREZZI = Path(r'C:\Users\L. MASI\Documents\Documenti_Attrezzi')


def estrai_dati(request):
    lavoratori = Formazione.objects.filter(lavoratore__in_forza=True).exclude(lavoratore__cognome='Ottomano')

    gruppi_lavoratori, n_gruppi_lavoratori = estrai_dati_util.dividi_elenco_lavoratori(lavoratori)

    formazione = (
        'preposto', 'primo_soccorso', 'antincendio', 'art37', 'spazi_confinati', 'ponteggiatore', 'imbracatore', 'mmc',
        'ept', 'dumper', 'rullo', 'autogru', 'gru_autocarro', 'carrello', 'sollevatore', 'ple', 'rls', 'aspp')

    gruppi_formazione, n_gruppi_formazione = estrai_dati_util.dividi_elenco_lavoratori(formazione, 3)

    nomine = ['nomina_{}'.format(x) for x in
              ('preposto', 'preposto_imbracatore', 'antincendio', 'primo_soccorso', 'aspp')]

    context = {'titolo': 'Estrai Dati',
               'sezione_utility_attiva': 'active',
               'pagina_attiva_estrai_dati': 'active',
               'n_gruppi_lavoratori': n_gruppi_lavoratori,
               'gruppi_lavoratori': gruppi_lavoratori,
               'n_gruppi_formazione': n_gruppi_formazione,
               'gruppi_formazione': gruppi_formazione,
               'nomine': nomine,
               }

    return render(request, 'utility/estrai_dati.html', context)


def dati_estratti(request):
    if request.method == 'POST':

        lavoratori = []
        attestati = []
        nomine = []
        documenti_vari = []
        for x in request.POST.keys():
            # ic(x)
            if x != 'csrfmiddlewaretoken':
                if x.isnumeric():
                    lavoratore = Formazione.objects.get(id__exact=x)
                    lavoratori.append(lavoratore)
                elif x.startswith('nomina_'):
                    nomine.append(x)
                elif x.startswith(('unilav', 'idoneita', 'consegna_dpi')):
                    documenti_vari.append(x)
                else:
                    attestati.append(x)

        dati = estrai_dati_util.Estrai_Dati()

        tabella, zip_file_nome, file_non_trovati = dati.estrai(lavoratori, attestati, nomine, documenti_vari)

        documenti_vari = ['Idoneità' if x == 'idoneita' else x for x in documenti_vari]

        documenti = attestati
        documenti.extend(nomine)
        documenti.extend(documenti_vari)

        context = {'titolo': 'Dati Estratti',
                   'sezione_utility_attiva': 'active',
                   'pagina_attiva_estrai_dati': 'active',
                   'lavoratori': lavoratori,
                   'documenti': documenti,
                   'tabella': tabella,
                   'zip': zip_file_nome,
                   'file_non_trovati': file_non_trovati
                   }

        return render(request, 'utility/dati_estratti.html', context)

    return


def documenti_controlla(request):
    context = {'titolo': 'Controlla Documenti',
               'sezione_utility_attiva': 'active',
               'pagina_attiva_controlla_documenti': 'active',
               }

    return render(request, 'utility/controlla_documenti_attendi.html', context)


def documenti_controllati(request):
    # --------------------------------------------------------------------------------------
    # Personale

    tipi_formazione = ('dirigente', 'preposto', 'primo_soccorso', 'antincendio', 'art37', 'spazi_confinati',
                       'ponteggiatore', 'imbracatore', 'mmc', 'ept', 'dumper', 'rullo', 'autogru', 'gru_autocarro',
                       'carrello', 'sollevatore', 'ple', 'rls', 'aspp')
    tipi_nomine = ('nomina_preposto', 'nomina_preposto_subappalti', 'nomina_preposto_imbracatore', 'nomina_antincendio',
                   'nomina_primo_soccorso', 'nomina_aspp')

    documenti_formazione = []
    documenti_nomine = []
    documenti_unilav = []
    documenti_idoneita = []
    documenti_consegna_dpi = []

    # Formazioni, nomine, unilav
    formazioni = Formazione.objects.filter(lavoratore__in_forza=True)

    for formazione in formazioni:
        lavoratore = formazione.lavoratore

        # formazione
        for tipo_formazione in tipi_formazione:
            data = getattr(formazione, f'{tipo_formazione}_dc')

            if data:
                data = data.strftime("%d%m%y")
                path_documento = PATH_DOCUMENTI_LAVORATORI / f'{lavoratore}' / 'attestati' / f'{tipo_formazione} {data}.pdf'
                documenti_formazione.append(path_documento)

        # nomine
        for tipo_nomina in tipi_nomine:
            data = getattr(formazione, tipo_nomina)

            if data:
                data = data.strftime("%d%m%y")
                path_documento = PATH_DOCUMENTI_LAVORATORI / f'{lavoratore}' / 'nomine' / f'{tipo_nomina} {data}.pdf'
                documenti_nomine.append(path_documento)

        # Contratto
        tipo_contratto = formazione.lavoratore.tipo_contratto
        match tipo_contratto:
            case 'T.I.' | 'T.I. - P. TIME':
                path_documento = PATH_DOCUMENTI_LAVORATORI / f'{lavoratore}' / 'unilav ind.pdf'
            case 'T.D.':
                path_documento = PATH_DOCUMENTI_LAVORATORI / f'{lavoratore}' / f'unilav {lavoratore.data_fine}.pdf'
            case _:
                path_documento = None
                ic(f'{lavoratore} ha un contratto non gestito')

        if path_documento:
            documenti_unilav.append(path_documento)

    # Idoneità
    idoneita_ = Idoneita.objects.filter(lavoratore__in_forza=True)

    for idoneita in idoneita_:
        data = getattr(idoneita, 'idoneita')

        if data:
            data = data.strftime("%d%m%y")
            path_documento = PATH_DOCUMENTI_LAVORATORI / f'{idoneita.lavoratore}' / f'idoneità {data}.pdf'
            documenti_idoneita.append(path_documento)

    # Consegna DPI
    dpi2 = DPI2.objects.filter(lavoratore__in_forza=True)

    for consegna in dpi2:
        data = getattr(consegna, 'consegna')

        if data:
            data = data.strftime("%d%m%y")
            path_documento = PATH_DOCUMENTI_LAVORATORI / f'{consegna.lavoratore}' / f'consegna_dpi {data}.pdf'
            documenti_consegna_dpi.append(path_documento)

    # Verifica esistenza file
    documenti_personale_non_trovati = []
    for elenco in (documenti_formazione, documenti_nomine, documenti_unilav, documenti_idoneita,
                   documenti_consegna_dpi):
        for doc in sorted(elenco):
            if not doc.exists():
                documenti_personale_non_trovati.append(doc)
                ic(doc.exists(), doc)

    # --------------------------------------------------------------------------------------
    # Mezzi
    documenti_mezzi = []

    elenco_mezzi = Mezzo.objects.filter(in_forza=True)
    campi = ('ce', 'ce_accessori', 'assicurazione', 'libretto', 'immatricolazione', 'libretto_inail', 'inail',
             'manuale')

    for mezzo in elenco_mezzi:
        for campo in campi:
            dato = getattr(mezzo, campo)

            if dato:
                match campo:
                    case 'ce' | 'ce_accessori' | 'libretto_inail' | 'manuale':
                        path_documento = PATH_DOCUMENTI_MEZZI / f'{mezzo}' / f'{campo}.pdf'

                    case 'assicurazione' | 'immatricolazione':
                        data = dato.strftime("%d%m%y")
                        path_documento = PATH_DOCUMENTI_MEZZI / f'{mezzo}' / f'{campo} {data}.pdf'

                    case 'libretto':
                        dato = getattr(mezzo, 'revisione')
                        if dato:
                            data = dato.strftime("%d%m%y")
                            path_documento = PATH_DOCUMENTI_MEZZI / f'{mezzo}' / f'libretto {data}.pdf'
                        else:
                            path_documento = PATH_DOCUMENTI_MEZZI / f'{mezzo}' / f'libretto.pdf'

                    case 'inail':
                        dato = datetime.date(dato.year - 1, dato.month, dato.day)

                        data = dato.strftime("%d%m%y")
                        path_documento = PATH_DOCUMENTI_MEZZI / f'{mezzo}' / f'verifica_periodica {data}.pdf'

                    case _:
                        path_documento = f'{mezzo}' / f'*** *** ***'

                if path_documento:
                    documenti_mezzi.append(path_documento)

    # Verifica esistenza file
    documenti_mezzi_non_trovati = []
    for doc in sorted(documenti_mezzi):
        if not doc.exists():
            documenti_mezzi_non_trovati.append(doc)
            ic(doc.exists(), doc)

    # --------------------------------------------------------------------------------------
    # Attrezzi
    documenti_attrezzi = []

    elenco_attrezzi = Attrezzo.objects.all()

    for attrezzo in elenco_attrezzi:
        for campo in ('ce', 'manuale'):
            dato = getattr(attrezzo, campo)
            if dato:
                path_documento = PATH_DOCUMENTI_ATTREZZI / f'{attrezzo.tipologia}' / f'{attrezzo}' / f'{campo}.pdf'
                documenti_attrezzi.append(path_documento)

    # ic(documenti_attrezzi)

    # Verifica esistenza file
    documenti_attrezzature_non_trovate = []
    for doc in documenti_attrezzi:
        if not doc.exists():
            documenti_attrezzature_non_trovate.append(doc)
            # ic(doc.exists(), doc)

    context = {'titolo': 'Controlla Documenti',
               'sezione_utility_attiva': 'active',
               'pagina_attiva_controlla_documenti': 'active',
               'documenti_personale_non_trovati': documenti_personale_non_trovati,
               'documenti_mezzi_non_trovati': documenti_mezzi_non_trovati,
               'documenti_attrezzature_non_trovate': documenti_attrezzature_non_trovate,
               }

    return render(request, 'utility/controlla_documenti_controllati.html', context)

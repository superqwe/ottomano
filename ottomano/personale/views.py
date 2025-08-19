import datetime
import glob
import itertools
import math
import os
import shutil
from pathlib import Path
from pprint import pprint as pp

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from icecream import ic
from personale import estrai_dati_util
from personale.models import Lavoratore, Formazione, Idoneita, DPI

from . import aggiorna_documenti_util

if settings.NOME_COMPUTER.lower() == 'srvdc1':
    PATH_DOCUMENTI = r'D:\Gestionale\Documenti_Lavoratori'
    PATH_BCK = r'D:\Gestionale'
else:
    PATH_DOCUMENTI = r'C:\Users\L. MASI\Documents\Documenti_Lavoratori'
    PATH_BCK = r'C:\Users\L. MASI\Documents\Programmi\ottomano\ottomano'

OGGI = datetime.date.today()
FRA_N_MESI = OGGI + datetime.timedelta(days=30.5 * 4)
FRA_1_MESI = OGGI + datetime.timedelta(days=30.5)
FRA_2_MESI = OGGI + datetime.timedelta(days=30.5 * 2)
FRA_3_MESI = OGGI + datetime.timedelta(days=30.5 * 3)
FRA_1_ANNO = OGGI + datetime.timedelta(days=365)
VECCHIO_DI_N_MESI = OGGI + datetime.timedelta(days=-30.5 * 1)
ANNO_CORRENTE = OGGI.year
ANNO_PROSSIMO = OGGI.year + 1


def backup_db():
    pathname = os.path.join(PATH_BCK, '*.sqlite3')
    db = glob.glob(pathname)
    backup_gia_effettuato = [True for x in db if Path(x).stem == f'bck_{OGGI}']

    if not backup_gia_effettuato:
        src = os.path.join(PATH_BCK, 'db.sqlite3')
        dst = os.path.join(PATH_BCK, f'bck_{OGGI}.sqlite3')

        shutil.copy2(src, dst)


def index(request):
    return HttpResponseRedirect("/personale/formazione")


def anagrafica(request):
    lavoratori = Lavoratore.objects.filter(in_forza=True)
    context = {'titolo': 'Anagrafica',
               'sezione_formazione_attiva': 'active',
               'pagina_attiva_anagrafica': 'active',
               'lavoratori': lavoratori}

    return render(request, './personale/anagrafica.html', context)


def formazione(request):
    backup_db()

    formazione_ = Formazione.objects. \
        filter(lavoratore__in_forza=True). \
        exclude(lavoratore__cognome='Ottomano'). \
        order_by('lavoratore__cantiere__nome', 'lavoratore__cognome', 'lavoratore__nome')

    context = {'titolo': 'Formazione',
               'pagina_attiva_formazione': 'active',
               'sezione_formazione_attiva': 'active',
               'formazione': formazione_,
               'conteggio_rg': conteggio_rg(formazione_),
               }

    return render(request, 'personale/formazione.html', context)


def aggiorna_documenti2(request):
    elenco_lavoratori = list(
        Lavoratore.objects.filter(in_forza=True).values_list('cognome', 'nome').order_by('cognome'))

    dir_lavoratori = [('%s %s' % lavoratore).lower() for lavoratore in elenco_lavoratori]

    lista_documenti = []
    for lavoratore in dir_lavoratori:

        # ricerca attestati
        path_attestati = os.path.join(PATH_DOCUMENTI, lavoratore, 'attestati')
        try:
            attestati = aggiorna_documenti_util.filtra_solo_documenti_nuovi(path_attestati)
            attestati = aggiorna_documenti_util.calcola_data_attestati(attestati, lavoratore)
        except FileNotFoundError:
            attestati = []

        cognome, nome = lavoratore.split(maxsplit=1)
        if attestati:
            formazione_ = Formazione.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)

            for corso, data_dc, data in attestati:
                setattr(formazione_, corso, data)
                setattr(formazione_, '%s_dc' % corso, data_dc)

            formazione_.save()

        # ricerca idoneità
        path_lavoratore = os.path.join(PATH_DOCUMENTI, lavoratore, 'idoneità *')

        try:
            path_idoneita = glob.glob(path_lavoratore)[0]

        except IndexError:
            print('*** manca idoneità *** %s' % lavoratore)

        if path_idoneita:
            idoneita_recente = aggiorna_documenti_util.verifica_se_recente(path_idoneita)

            if idoneita_recente:
                scadenza_idoneita = Path(path_idoneita).stem.split()[1]
                scadenza_idoneita = datetime.datetime.strptime(scadenza_idoneita, '%d%m%y')

                attestati.append(('idoneità', scadenza_idoneita, None))

                idoneita = Idoneita.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)
                idoneita.idoneita = scadenza_idoneita
                idoneita.save()

        # ricerca nomine
        try:
            path_nomine = os.path.join(PATH_DOCUMENTI, lavoratore, 'nomine')

            nomine = aggiorna_documenti_util.filtra_solo_documenti_nuovi(path_nomine)

            if nomine:
                formazione = Formazione.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)

                for nomina in nomine:
                    tipo_nomina, data_nomina = os.path.splitext(nomina)[0].split()
                    data_nomina = datetime.datetime.strptime(data_nomina, '%d%m%y')

                    match tipo_nomina:
                        case 'nomina_preposto':
                            formazione.nomina_preposto = data_nomina
                        case 'nomina_preposto_subappalti':
                            formazione.nomina_preposto_subappalti = data_nomina
                        case 'nomina_preposto_imbracatore':
                            formazione.nomina_preposto_imbracatore = data_nomina
                        case 'nomina_antincendio':
                            formazione.nomina_antincendio = data_nomina
                        case 'nomina_primo_soccorso':
                            formazione.nomina_primo_soccorso = data_nomina

                    formazione.save()

        except FileNotFoundError:
            pass

        lista_documenti.append([lavoratore, attestati])

    os.chdir(PATH_DOCUMENTI)

    context = {'titolo': 'Aggiorna Documenti',
               'sezione_formazione_attiva': 'active',
               'pagina_attiva_aggiorna_documenti': 'active',
               'lista_documenti': lista_documenti}

    return render(request, 'personale/aggiorna_documenti.html', context)


# todo: obsoleto
# def aggiorna_stato(request):
#     Formazione.objects.filter(lavoratore__in_forza=True).update(stato='verde')
#
#     # art37 se ha la formazione da aspp
#     Formazione.objects.filter(Q(lavoratore__in_forza=True) & Q(art37__lt=OGGI) & Q(aspp__gt=OGGI)).update(
#         art37_ck='es-aspp')
#     # art37 se ha la formazione da preposto
#     Formazione.objects.filter(Q(lavoratore__in_forza=True) & Q(art37__lt=OGGI) & Q(preposto__gt=OGGI)).update(
#         art37_ck='es-prep')
#
#     Formazione.objects.filter(Q(dirigente__gt=OGGI) | Q(dirigente__isnull=True)).update(dirigente_ck='')
#     Formazione.objects.filter(Q(preposto__gt=OGGI) | Q(preposto__isnull=True)).update(preposto_ck='')
#     Formazione.objects.filter(Q(primo_soccorso__gt=OGGI) | Q(primo_soccorso__isnull=True)).update(primo_soccorso_ck='')
#     Formazione.objects.filter(Q(antincendio__gt=OGGI) | Q(antincendio__isnull=True)).update(antincendio_ck='')
#     Formazione.objects.filter(Q(art37__gt=OGGI) | Q(art37__isnull=True)).update(art37_ck='')
#     Formazione.objects.filter(Q(spazi_confinati__gt=OGGI) | Q(spazi_confinati__isnull=True)).update(
#         spazi_confinati_ck='')
#     Formazione.objects.filter(Q(ponteggiatore__gt=OGGI) | Q(ponteggiatore__isnull=True)).update(ponteggiatore_ck='')
#     Formazione.objects.filter(Q(imbracatore__gt=OGGI) | Q(imbracatore__isnull=True)).update(imbracatore_ck='')
#     Formazione.objects.filter(Q(mmc__gt=OGGI) | Q(mmc__isnull=True)).update(mmc_ck='')
#     Formazione.objects.filter(Q(ept__gt=OGGI) | Q(ept__isnull=True)).update(ept_ck='')
#     Formazione.objects.filter(Q(autogru__gt=OGGI) | Q(autogru__isnull=True)).update(autogru_ck='')
#     Formazione.objects.filter(Q(gru_autocarro__gt=OGGI) | Q(gru_autocarro__isnull=True)).update(gru_autocarro_ck='')
#     Formazione.objects.filter(Q(carrello__gt=OGGI) | Q(carrello__isnull=True)).update(carrello_ck='')
#     Formazione.objects.filter(Q(sollevatore__gt=OGGI) | Q(sollevatore__isnull=True)).update(sollevatore_ck='')
#     Formazione.objects.filter(Q(ple__gt=OGGI) | Q(ple__isnull=True)).update(ple_ck='')
#     Formazione.objects.filter(Q(rls__gt=OGGI) | Q(rls__isnull=True)).update(rls_ck='')
#     Formazione.objects.filter(Q(aspp__gt=OGGI) | Q(aspp__isnull=True)).update(aspp_ck='')
#
#     Formazione.objects.filter(dirigente__lt=FRA_N_MESI).update(dirigente_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(preposto__lt=FRA_N_MESI).update(preposto_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(primo_soccorso__lt=FRA_N_MESI).update(primo_soccorso_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(antincendio__lt=FRA_N_MESI).update(antincendio_ck='table-warning', stato='giallo')
#     Formazione.objects. \
#         filter(art37__lt=FRA_N_MESI). \
#         exclude(art37_ck__in=['es-aspp', 'es-prep']). \
#         update(art37_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(spazi_confinati__lt=FRA_N_MESI).update(spazi_confinati_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(ponteggiatore__lt=FRA_N_MESI).update(ponteggiatore_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(imbracatore__lt=FRA_N_MESI).update(imbracatore_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(mmc__lt=FRA_N_MESI).update(mmc_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(ept__lt=FRA_N_MESI).update(ept_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(autogru__lt=FRA_N_MESI).update(autogru_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(gru_autocarro__lt=FRA_N_MESI).update(gru_autocarro_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(carrello__lt=FRA_N_MESI).update(carrello_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(sollevatore__lt=FRA_N_MESI).update(sollevatore_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(ple__lt=FRA_N_MESI).update(ple_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(rls__lt=FRA_N_MESI).update(rls_ck='table-warning', stato='giallo')
#     Formazione.objects.filter(aspp__lt=FRA_N_MESI).update(aspp_ck='table-warning', stato='giallo')
#
#     Formazione.objects.filter(dirigente__lt=OGGI).update(dirigente_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(preposto__lt=OGGI).update(preposto_ck='table-danger', stato='rosso')
#     Formazione.objects. \
#         filter(art37__lt=OGGI). \
#         exclude(art37_ck__in=['es-aspp', 'es-prep']). \
#         update(art37_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(primo_soccorso__lt=OGGI).update(primo_soccorso_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(antincendio__lt=OGGI).update(antincendio_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(spazi_confinati__lt=OGGI).update(spazi_confinati_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(ponteggiatore__lt=OGGI).update(ponteggiatore_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(imbracatore__lt=OGGI).update(imbracatore_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(mmc__lt=OGGI).update(mmc_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(ept__lt=OGGI).update(ept_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(autogru__lt=OGGI).update(autogru_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(gru_autocarro__lt=OGGI).update(gru_autocarro_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(carrello__lt=OGGI).update(carrello_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(sollevatore__lt=OGGI).update(sollevatore_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(ple__lt=OGGI).update(ple_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(rls__lt=OGGI).update(rls_ck='table-danger', stato='rosso')
#     Formazione.objects.filter(aspp__lt=OGGI).update(aspp_ck='table-danger', stato='rosso')
#
#     # Formazione.objects.filter(art37=None).update(art37_ck='table-danger', stato='rosso')
#
#     Idoneita.objects.filter(idoneita__gt=OGGI).update(idoneita_ck='')
#     Idoneita.objects.filter(idoneita__lt=FRA_1_MESI).update(idoneita_ck='table-warning')
#     Idoneita.objects.filter(Q(idoneita__lt=OGGI) | Q(idoneita__isnull=True)).update(idoneita_ck='table-danger')
#     # Idoneita.objects.filter(idoneita=None).update(idoneita_ck='table-danger')
#     # Idoneita.objects.filter(idoneita__lt=OGGI).update(idoneita_ck='table-danger')
#
#     result = None
#
#     context = {'titolo': 'Aggiorna Stato',
#                'sezione_formazione_attiva': 'active',
#                'pagina_attiva_aggiorna_stato': 'active',
#                'dati': result,
#                }
#
#     return render(request, 'personale/aggiorna_stato.html', context)


def aggiorna_stato2(request):
    Formazione.objects.filter(lavoratore__in_forza=True).update(stato='verde')

    campi_ck = [
        'dirigente', 'preposto', 'primo_soccorso', 'antincendio', 'spazi_confinati',
        'ponteggiatore', 'imbracatore', 'mmc', 'ept', 'autogru', 'gru_autocarro',
        'carrello', 'sollevatore', 'ple', 'rls', 'aspp'
    ]

    for campo in campi_ck:
        kwargs_null = {f"{campo}__isnull": True}
        kwargs_future = {f"{campo}__gt": OGGI}
        kwargs_warning = {f"{campo}__lt": FRA_N_MESI}
        kwargs_danger = {f"{campo}__lt": OGGI}

        Formazione.objects.filter(Q(**kwargs_null) | Q(**kwargs_future)).update(**{f"{campo}_ck": ''})
        Formazione.objects.filter(**kwargs_warning).update(**{f"{campo}_ck": 'table-warning', 'stato': 'giallo'})
        Formazione.objects.filter(**kwargs_danger).update(**{f"{campo}_ck": 'table-danger', 'stato': 'rosso'})

    # art37
    Formazione.objects.filter(
        Q(lavoratore__in_forza=True) & Q(art37__lt=OGGI) & Q(aspp__gt=OGGI)).update(art37_ck='es-aspp')
    Formazione.objects.filter(
        Q(lavoratore__in_forza=True) & Q(art37__lt=OGGI) & Q(preposto__gt=OGGI)).update(art37_ck='es-prep')
    Formazione.objects.filter(Q(art37__gt=OGGI) | Q(art37__isnull=True)).update(art37_ck='')
    Formazione.objects.filter(art37__lt=FRA_N_MESI).exclude(art37_ck__in=['es-aspp', 'es-prep']).update(
        art37_ck='table-warning', stato='giallo')

    # Danger
    Formazione.objects.filter(art37__lt=OGGI).exclude(art37_ck__in=['es-aspp', 'es-prep']).update(
        art37_ck='table-danger', stato='rosso')

    # idoneita'
    Idoneita.objects.filter(idoneita__gt=OGGI).update(idoneita_ck='')
    Idoneita.objects.filter(idoneita__lt=FRA_1_MESI).update(idoneita_ck='table-warning')
    Idoneita.objects.filter(Q(idoneita__lt=OGGI) | Q(idoneita__isnull=True)).update(idoneita_ck='table-danger')

    context = {'titolo': 'Aggiorna Stato',
               'sezione_formazione_attiva': 'active',
               'pagina_attiva_aggiorna_stato': 'active',
               }

    return redirect('/personale/formazione')


def idoneita(request):
    idoneita = Idoneita.objects.filter(lavoratore__in_forza=True).exclude(lavoratore__cognome='Ottomano')
    # print(formazione)
    context = {'titolo': 'Idoneità',
               'sezione_formazione_attiva': 'active',
               'pagina_attiva_idoneita': 'active',
               'idoneita': idoneita}

    return render(request, 'personale/idoneita.html', context)


def scadenziario_formazione(request):
    lavoratori = Formazione.objects. \
        filter(lavoratore__in_forza=True, stato__in=['giallo', 'rosso']). \
        order_by('lavoratore__cantiere__nome', '-stato', 'lavoratore__cognome', 'lavoratore__nome')

    context = {'titolo': 'Scadenziario Formazione',
               'sezione_formazione_attiva': 'active',
               'pagina_attiva_scadenziario_formazione': 'active',
               'formazione': lavoratori,
               'conteggio_rg': conteggio_rg(lavoratori)}

    return render(request, 'personale/formazione.html', context)


def scadenzario_idoneita(request):
    idoneita = Idoneita.objects. \
        filter(lavoratore__in_forza=True, idoneita__lt=FRA_3_MESI). \
        order_by('idoneita', 'lavoratore__cognome', 'lavoratore__nome')

    context = {'titolo': 'Scadenzario Idoneità',
               'sezione_formazione_attiva': 'active',
               'pagina_attiva_scadenzario_idoneita': 'active',
               'idoneita': idoneita}

    return render(request, 'personale/idoneita.html', context)


def estrai_dati(request):
    lavoratori = Formazione.objects.filter(lavoratore__in_forza=True).exclude(
        lavoratore__cantiere__cantiere='Uffici Sede')

    gruppi_lavoratori, n_gruppi_lavoratori = estrai_dati_util.dividi_elenco_lavoratori(lavoratori)

    formazione = (
        'preposto', 'primo_soccorso', 'antincendio', 'art37', 'spazi_confinati', 'ponteggiatore', 'imbracatore', 'mmc',
        'ept', 'dumper', 'rullo', 'autogru', 'gru_autocarro', 'carrello', 'sollevatore', 'ple', 'rls', 'aspp')

    gruppi_formazione, n_gruppi_formazione = estrai_dati_util.dividi_elenco_lavoratori(formazione, 3)

    nomine = ['nomina_{}'.format(x) for x in
              ('preposto', 'preposto_imbracatore', 'antincendio', 'primo_soccorso', 'aspp')]
    # gruppi_nomine, n_gruppi_nomine = estrai_dati_util.dividi_elenco_lavoratori(nomine)

    context = {'titolo': 'Estrai Dati',
               'sezione_formazione_attiva': 'active',
               'pagina_attiva_estrai_dati': 'active',
               'n_gruppi_lavoratori': n_gruppi_lavoratori,
               'gruppi_lavoratori': gruppi_lavoratori,
               'n_gruppi_formazione': n_gruppi_formazione,
               'gruppi_formazione': gruppi_formazione,
               'nomine': nomine,
               # 'n_gruppi_nomine': n_gruppi_nomine,
               # 'gruppi_nomine': gruppi_nomine,
               }

    return render(request, 'personale/estrai_dati.html', context)


def dati_estratti(request):
    if request.method == 'POST':

        lavoratori = []
        attestati = []
        nomine = []
        for x in request.POST.keys():
            # print(x)
            if x != 'csrfmiddlewaretoken':
                if x.isnumeric():
                    lavoratore = Formazione.objects.get(id__exact=x)
                    lavoratori.append(lavoratore)
                elif x.startswith('nomina_'):
                    nomine.append(x)
                else:
                    attestati.append(x)

        dati = estrai_dati_util.Estrai_Dati()
        # dati.salva_lavoratori(lavoratori)

        # print()
        # pp(attestati)
        # print()

        tabella, zip_file_nome = dati.estrai(lavoratori, attestati, nomine)

        documenti = attestati
        documenti.extend(nomine)

        context = {'titolo': 'Dati Estratti',
                   'sezione_formazione_attiva': 'active',
                   'pagina_attiva_estrai_dati': 'active',
                   'lavoratori': lavoratori,
                   'documenti': documenti,
                   'tabella': tabella,
                   'zip': zip_file_nome
                   }

        return render(request, 'personale/dati_estratti.html', context)

    return


def conteggio_rg(query):
    stato_r = query.filter(stato='rosso').count()
    stato_g = query.filter(stato='giallo').count()
    art37_r = query.filter(art37_ck='table-danger').count()
    art37_g = query.filter(art37_ck='table-warning').count()
    preposto_r = query.filter(preposto_ck='table-danger').count()
    preposto_g = query.filter(preposto_ck='table-warning').count()
    dirigente_r = query.filter(dirigente_ck='table-danger').count()
    dirigente_g = query.filter(dirigente_ck='table-warning').count()
    antincendio_r = query.filter(antincendio_ck='table-danger').count()
    antincendio_g = query.filter(antincendio_ck='table-warning').count()
    spazi_confinati_r = query.filter(spazi_confinati_ck='table-danger').count()
    spazi_confinati_g = query.filter(spazi_confinati_ck='table-warning').count()
    primo_soccorso_r = query.filter(primo_soccorso_ck='table-danger').count()
    primo_soccorso_g = query.filter(primo_soccorso_ck='table-warning').count()
    ponteggiatore_r = query.filter(ponteggiatore_ck='table-danger').count()
    ponteggiatore_g = query.filter(ponteggiatore_ck='table-warning').count()
    imbracatore_r = query.filter(imbracatore_ck='table-danger').count()
    imbracatore_g = query.filter(imbracatore_ck='table-warning').count()
    mmc_r = query.filter(mmc_ck='table-danger').count()
    mmc_g = query.filter(mmc_ck='table-warning').count()
    ept_r = query.filter(ept_ck='table-danger').count()
    ept_g = query.filter(ept_ck='table-warning').count()
    autogru_r = query.filter(autogru_ck='table-danger').count()
    autogru_g = query.filter(autogru_ck='table-warning').count()
    gru_autocarro_r = query.filter(gru_autocarro_ck='table-danger').count()
    gru_autocarro_g = query.filter(gru_autocarro_ck='table-warning').count()
    carrello_r = query.filter(carrello_ck='table-danger').count()
    carrello_g = query.filter(carrello_ck='table-warning').count()
    sollevatore_r = query.filter(sollevatore_ck='table-danger').count()
    sollevatore_g = query.filter(sollevatore_ck='table-warning').count()
    ple_r = query.filter(ple_ck='table-danger').count()
    ple_g = query.filter(ple_ck='table-warning').count()

    conteggio = {
        'stato_r': stato_r,
        'stato_g': stato_g,
        'art37_r': art37_r,
        'art37_g': art37_g,
        'preposto_r': preposto_r,
        'preposto_g': preposto_g,
        'dirigente_r': dirigente_r,
        'dirigente_g': dirigente_g,
        'antincendio_r': antincendio_r,
        'antincendio_g': antincendio_g,
        'spazi_confinati_r': spazi_confinati_r,
        'spazi_confinati_g': spazi_confinati_g,
        'primo_soccorso_r': primo_soccorso_r,
        'primo_soccorso_g': primo_soccorso_g,
        'ponteggiatore_r': ponteggiatore_r,
        'ponteggiatore_g': ponteggiatore_g,
        'imbracatore_r': imbracatore_r,
        'imbracatore_g': imbracatore_g,
        'mmc_r': mmc_r,
        'mmc_g': mmc_g,
        'ept_r': ept_r,
        'ept_g': ept_g,
        'autogru_r': autogru_r,
        'autogru_g': autogru_g,
        'gru_autocarro_r': gru_autocarro_r,
        'gru_autocarro_g': gru_autocarro_g,
        'carrello_r': carrello_r,
        'carrello_g': carrello_g,
        'sollevatore_r': sollevatore_r,
        'sollevatore_g': sollevatore_g,
        'ple_r': ple_r,
        'ple_g': ple_g,
    }

    return conteggio


def scadenzario_dpi(request):
    dpi = DPI.objects. \
        filter(lavoratore__in_forza=True, ). \
        exclude(lavoratore__cantiere__cantiere='Uffici Sede'). \
        order_by('lavoratore__cantiere', 'lavoratore__cognome', 'lavoratore__nome')

    context = {'titolo': 'Scadenzario DPI',
               'sezione_formazione_attiva': 'active',
               'pagina_attiva_scadenzario_dpi': 'active',
               'lista_dpi': dpi}

    return render(request, 'personale/scadenzario_dpi.html', context)


def scadenzario_formazione_schede(request, anno):
    # todo: obsoleta
    def my_sort(sub_li):
        sub_li.sort(key=lambda x: x[2])
        return sub_li

    def dividi_liste(lista_lunga, lunghezza_massima_lista):
        lista_lunga = iter(lista_lunga)
        return iter(lambda: tuple(itertools.islice(lista_lunga, lunghezza_massima_lista)), ())

    def conteggio(elenco):
        filtra = [x[3] for x in elenco]
        return (filtra.count(''), filtra.count('text-warning'), filtra.count('text-danger'), len(filtra),
                math.ceil(len(filtra) / 10) * 2)

    # todo: obsoleta
    def conteggio2(elenco):
        filtra = [x[3] for x in elenco]
        return filtra.count(''), filtra.count('text-warning'), filtra.count('text-danger'), len(filtra)

    def card_ordinate_per_n_elementi(elenco):
        elenco.sort(key=lambda x: x[2][3])
        return reversed(elenco)

    if anno == 'corrente':
        scadenza_formazione = datetime.date(ANNO_CORRENTE, 12, 31)
    else:
        scadenza_formazione = datetime.date(ANNO_PROSSIMO, 12, 31)

    lista_corsi = ('dirigente', 'preposto', 'primo_soccorso', 'antincendio', 'art37', 'spazi_confinati',
                   'ponteggiatore', 'imbracatore', 'mmc', 'ept', 'dumper', 'rullo', 'autogru', 'gru_autocarro',
                   'carrello', 'sollevatore', 'ple', 'rls', 'aspp')

    scadenze = []
    for corso in lista_corsi:
        corso_ck = '%s_ck' % corso

        scade_tra_1_anno = Q(**{'%s__lt' % corso: scadenza_formazione})
        lavoratori = Formazione.objects.filter(scade_tra_1_anno).filter(lavoratore__in_forza=True)

        # esonero art37 #####
        if corso == 'art37':
            # per i preposti
            lavoratori = [x for x in lavoratori if x.preposto is None or x.preposto <= x.art37]

            # per gli aspp
            lavoratori = [x for x in lavoratori if x.aspp is None or x.aspp <= x.art37]
        #####################

        if lavoratori:
            elenco_lavoratori = [[x.lavoratore.cognome, x.lavoratore.nome, getattr(x, corso), getattr(x, corso_ck)]
                                 for x in lavoratori
                                 ]

            elenco_lavoratori_ = []
            for lavoratore in elenco_lavoratori:
                cognome, nome, scadenza_corso, colore_corso = lavoratore

                if colore_corso:
                    colore_corso = colore_corso.replace('table', 'text')

                lavoratori_ = cognome, nome, scadenza_corso, colore_corso
                elenco_lavoratori_.append(lavoratori_)

                elenco_lavoratori_.sort(key=lambda x: x[2])  # ordina per data di scadenza

            scadenze.append((corso, elenco_lavoratori_, conteggio(elenco_lavoratori_)))

    scadenze = card_ordinate_per_n_elementi(scadenze)

    card = []
    for scadenza in scadenze:
        scadenza_ = list(scadenza)
        elenco_lavoratori_a_tranci = list(dividi_liste(scadenza_[1], 10))
        scadenza_[1] = elenco_lavoratori_a_tranci
        card.append(scadenza_)

    context = {'titolo': 'Scadenziario Formazione',
               'sezione_formazione_attiva': 'active',
               'pagina_attiva_scadenziario_formazione': 'active',
               'scadenze': card,
               'conteggio_rg': conteggio_rg(lavoratori)}

    if anno == 'corrente':
        context['pagina_attiva_formazione_corrente'] = 'active'
    else:
        context['pagina_attiva_formazione_prossimo'] = 'active'

    return render(request, 'personale/formazione_schede.html', context)

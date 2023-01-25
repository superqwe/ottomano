import datetime
import glob
import os

# import personale.importa_dati
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from personale import aggiorna_documenti_util
from personale.models import Lavoratore, Formazione, Idoneita

from pprint import pprint as pp

from personale import estrai_dati_util

PATH_DOCUMENTI = r'C:\Users\L. MASI\Documents\Documenti_Lavoratori'
# PATH_DOCUMENTI = r'z:\Documenti_Lavoratori'
OGGI = datetime.date.today()
FRA_N_MESI = OGGI + datetime.timedelta(days=30.5 * 3)
FRA_1_MESI = OGGI + datetime.timedelta(days=30.5)
FRA_2_MESI = OGGI + datetime.timedelta(days=30.5 * 2)


def index(request):
    return HttpResponse("Hello, world. You're at the personale index.")


def anagrafica(request):
    lavoratori = Lavoratore.objects.filter(in_forza=True)
    context = {'titolo': 'Anagrafica',
               'pagina_attiva_anagrafica': 'active',
               'lavoratori': lavoratori}

    return render(request, 'base.html', context)


def formazione(request):
    formazione_ = Formazione.objects. \
        filter(lavoratore__in_forza=True). \
        order_by('lavoratore__cantiere__nome', 'lavoratore__cognome', 'lavoratore__nome')

    context = {'titolo': 'Formazione',
               'pagina_attiva_formazione': 'active',
               'formazione': formazione_,
               'conteggio_rg': conteggio_rg(formazione_)}

    return render(request, 'personale/formazione.html', context)


def aggiorna_documenti(request):
    # verifica se sono presenti nuovi lavoratori
    elenco_lavoratori = Lavoratore.objects.all().values_list('cognome', 'nome').order_by('cognome')
    elenco_lavoratori = [('%s %s' % lavoratore).lower() for lavoratore in elenco_lavoratori]

    dir_lavoratori = os.listdir(PATH_DOCUMENTI)
    dir_lavoratori = [lavoratore.lower() for lavoratore in dir_lavoratori]

    nuovi_lavoratori = []
    lista_documenti = []
    for lavoratore in dir_lavoratori:
        # print(lavoratore)

        if not lavoratore in elenco_lavoratori:
            path_dir_lavoratore = os.path.join(PATH_DOCUMENTI, lavoratore)

            if os.path.isdir(path_dir_lavoratore):
                nuovi_lavoratori.append(lavoratore)
                print('\n' * 3, 'Nuovo lavoratore', lavoratore.split(maxsplit=1), '\n' * 3)
                cognome, nome = lavoratore.split(maxsplit=1)

                nuovo_lavoratore = Lavoratore(cognome=cognome.title(), nome=nome.title())
                nuovo_lavoratore.save()

                nuovo_lavoratore_idoneita = Idoneita(lavoratore=nuovo_lavoratore)
                nuovo_lavoratore_idoneita.save()
            else:
                continue

        # ricerca attestati
        path_attestati = os.path.join(PATH_DOCUMENTI, lavoratore, 'attestati')
        try:
            attestati = os.listdir(path_attestati)
            attestati = aggiorna_documenti_util.calcola_data_attestati(attestati, lavoratore)
        except FileNotFoundError:
            attestati = []

        # salva su db
        if attestati or True:
            cognome, nome = lavoratore.split(maxsplit=1)

            try:
                formazione_ = Formazione.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)
                # print('----->', formazione_)
            except ObjectDoesNotExist:
                lavoratore = Lavoratore.objects.get(cognome__iexact=cognome, nome__iexact=nome)
                formazione_ = Formazione(lavoratore=lavoratore)

            for corso, data_dc, data in attestati:
                # print(attestati)
                # print(corso)
                setattr(formazione_, corso, data)
                setattr(formazione_, '%s_dc' % corso, data_dc)

            formazione_.save()

        # ricerca idoneità
        try:
            path_lavoratore = os.path.join(PATH_DOCUMENTI, lavoratore)
        except TypeError:
            # todo: eccezione da gestire
            print('*** errore nella ricerca dell\'idoneità di ', lavoratore)

        os.chdir(path_lavoratore)
        lfile = glob.glob('idoneità*')

        try:
            idoneita = Idoneita.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)
        except ObjectDoesNotExist:
            lavoratore = Lavoratore.objects.get(cognome__iexact=cognome, nome__iexact=nome)
            idoneita = Idoneita(lavoratore=lavoratore)

        match len(lfile):
            case 1:
                scadenza_idoneita = os.path.splitext(lfile[0])[0].split()[1]
                scadenza_idoneita = datetime.datetime.strptime(scadenza_idoneita, '%d%m%y')
                idoneita.idoneita = scadenza_idoneita

                attestati.append(('idoneità', scadenza_idoneita, None))

            case 0:
                print('*** manca idoneità *** %s' % lavoratore)
            case _:
                print('*** più di una idoneità *** %s' % lavoratore)

        idoneita.save()

        # ricerca nomine

        try:
            path_nomine = os.path.join(PATH_DOCUMENTI, lavoratore, 'nomine')
            nomine = os.listdir(path_nomine)

            for nomina in nomine:
                tipo_nomina, data_nomina = os.path.splitext(nomina)[0].split()
                data_nomina = datetime.datetime.strptime(data_nomina, '%d%m%y')

                formazione = Formazione.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)

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

        ###
        lista_documenti.append([lavoratore, attestati])

    # pp(lista_documenti)

    os.chdir(PATH_DOCUMENTI)

    context = {'titolo': 'Aggiorna Documenti',
               'pagina_attiva_aggiorna_documenti': 'active',
               'lista_documenti': lista_documenti}

    return render(request, 'personale/aggiorna_documenti.html', context)


def aggiorna_stato(request):
    Formazione.objects.filter(lavoratore__in_forza=True).update(stato='verde')

    Formazione.objects.filter(dirigente__gt=OGGI).update(dirigente_ck='')
    Formazione.objects.filter(preposto__gt=OGGI).update(preposto_ck='')
    Formazione.objects.filter(primo_soccorso__gt=OGGI).update(primo_soccorso_ck='')
    Formazione.objects.filter(antincendio__gt=OGGI).update(antincendio_ck='')
    Formazione.objects.filter(art37__gt=OGGI).update(art37_ck='')
    Formazione.objects.filter(spazi_confinati__gt=OGGI).update(spazi_confinati_ck='')
    Formazione.objects.filter(ponteggiatore__gt=OGGI).update(ponteggiatore_ck='')
    Formazione.objects.filter(imbracatore__gt=OGGI).update(imbracatore_ck='')
    Formazione.objects.filter(ept__gt=OGGI).update(ept_ck='')
    Formazione.objects.filter(autogru__gt=OGGI).update(autogru_ck='')
    Formazione.objects.filter(gru_autocarro__gt=OGGI).update(gru_autocarro_ck='')
    Formazione.objects.filter(carrello__gt=OGGI).update(carrello_ck='')
    Formazione.objects.filter(sollevatore__gt=OGGI).update(sollevatore_ck='')
    Formazione.objects.filter(ple__gt=OGGI).update(ple_ck='')
    Formazione.objects.filter(rls__gt=OGGI).update(rls_ck='')
    Formazione.objects.filter(aspp__gt=OGGI).update(aspp_ck='')

    Formazione.objects.filter(dirigente__lt=FRA_N_MESI).update(dirigente_ck='table-warning', stato='giallo')
    Formazione.objects.filter(preposto__lt=FRA_N_MESI).update(preposto_ck='table-warning', stato='giallo')
    Formazione.objects.filter(primo_soccorso__lt=FRA_N_MESI).update(primo_soccorso_ck='table-warning', stato='giallo')
    Formazione.objects.filter(antincendio__lt=FRA_N_MESI).update(antincendio_ck='table-warning', stato='giallo')
    Formazione.objects.filter(art37__lt=FRA_N_MESI).update(art37_ck='table-warning', stato='giallo')
    Formazione.objects.filter(spazi_confinati__lt=FRA_N_MESI).update(spazi_confinati_ck='table-warning', stato='giallo')
    Formazione.objects.filter(ponteggiatore__lt=FRA_N_MESI).update(ponteggiatore_ck='table-warning', stato='giallo')
    Formazione.objects.filter(imbracatore__lt=FRA_N_MESI).update(imbracatore_ck='table-warning', stato='giallo')
    Formazione.objects.filter(ept__lt=FRA_N_MESI).update(ept_ck='table-warning', stato='giallo')
    Formazione.objects.filter(autogru__lt=FRA_N_MESI).update(autogru_ck='table-warning', stato='giallo')
    Formazione.objects.filter(gru_autocarro__lt=FRA_N_MESI).update(gru_autocarro_ck='table-warning', stato='giallo')
    Formazione.objects.filter(carrello__lt=FRA_N_MESI).update(carrello_ck='table-warning', stato='giallo')
    Formazione.objects.filter(sollevatore__lt=FRA_N_MESI).update(sollevatore_ck='table-warning', stato='giallo')
    Formazione.objects.filter(ple__lt=FRA_N_MESI).update(ple_ck='table-warning', stato='giallo')
    Formazione.objects.filter(rls__lt=FRA_N_MESI).update(rls_ck='table-warning', stato='giallo')
    Formazione.objects.filter(aspp__lt=FRA_N_MESI).update(aspp_ck='table-warning', stato='giallo')

    Formazione.objects.filter(dirigente__lt=OGGI).update(dirigente_ck='table-danger', stato='rosso')
    Formazione.objects.filter(preposto__lt=OGGI).update(preposto_ck='table-danger', stato='rosso')
    Formazione.objects.filter(primo_soccorso__lt=OGGI).update(primo_soccorso_ck='table-danger', stato='rosso')
    Formazione.objects.filter(antincendio__lt=OGGI).update(antincendio_ck='table-danger', stato='rosso')
    Formazione.objects.filter(art37__lt=OGGI).update(art37_ck='table-danger', stato='rosso')
    Formazione.objects.filter(spazi_confinati__lt=OGGI).update(spazi_confinati_ck='table-danger', stato='rosso')
    Formazione.objects.filter(ponteggiatore__lt=OGGI).update(ponteggiatore_ck='table-danger', stato='rosso')
    Formazione.objects.filter(imbracatore__lt=OGGI).update(imbracatore_ck='table-danger', stato='rosso')
    Formazione.objects.filter(ept__lt=OGGI).update(ept_ck='table-danger', stato='rosso')
    Formazione.objects.filter(autogru__lt=OGGI).update(autogru_ck='table-danger', stato='rosso')
    Formazione.objects.filter(gru_autocarro__lt=OGGI).update(gru_autocarro_ck='table-danger', stato='rosso')
    Formazione.objects.filter(carrello__lt=OGGI).update(carrello_ck='table-danger', stato='rosso')
    Formazione.objects.filter(ple__lt=OGGI).update(ple_ck='table-danger', stato='rosso')
    Formazione.objects.filter(rls__lt=OGGI).update(rls_ck='table-danger', stato='rosso')
    Formazione.objects.filter(aspp__lt=OGGI).update(aspp_ck='table-danger', stato='rosso')

    Formazione.objects.filter(art37=None).update(art37_ck='table-danger', stato='rosso')

    Idoneita.objects.filter(idoneita__gt=OGGI).update(idoneita_ck='')
    Idoneita.objects.filter(idoneita__lt=FRA_1_MESI).update(idoneita_ck='table-warning')
    Idoneita.objects.filter(idoneita=None).update(idoneita_ck='table-danger')
    Idoneita.objects.filter(idoneita__lt=OGGI).update(idoneita_ck='table-danger')

    result = None

    context = {'titolo': 'Aggiorna Stato',
               'pagina_attiva_aggiorna_stato': 'active',
               'dati': result,
               }

    return render(request, 'personale/aggiorna_stato.html', context)


def idoneita(request):
    idoneita = Idoneita.objects.filter(lavoratore__in_forza=True)
    # print(formazione)
    context = {'titolo': 'Idoneità',
               'pagina_attiva_idoneita': 'active',
               'idoneita': idoneita}

    return render(request, 'personale/idoneita.html', context)


def scadenziario_formazione(request):
    lavoratori = Formazione.objects. \
        filter(lavoratore__in_forza=True, stato__in=['giallo', 'rosso']). \
        order_by('-stato', 'lavoratore__cognome', 'lavoratore__nome')

    context = {'titolo': 'Scadenziario Formazione',
               'pagina_attiva_scadenziario_formazione': 'active',
               'formazione': lavoratori,
               'conteggio_rg': conteggio_rg(lavoratori)}

    return render(request, 'personale/formazione.html', context)


def scadenziario_formazione2(request):
    context = {'titolo': 'Scadenziario Formazione',
               'pagina_attiva_scadenziario_formazione': 'active',}

    return render(request, 'personale/formazione.html', context)


def scadenziario_idoneita(request):
    idoneita = Idoneita.objects. \
        filter(lavoratore__in_forza=True, idoneita__lt=FRA_2_MESI). \
        order_by('idoneita', 'lavoratore__cognome', 'lavoratore__nome')

    context = {'titolo': 'Scadenzario Idoneità',
               'pagina_attiva_scadenziario_idoneita': 'active',
               'idoneita': idoneita}

    return render(request, 'personale/idoneita.html', context)


def estrai_dati(request):
    lavoratori = Formazione.objects.filter(lavoratore__in_forza=True).exclude(lavoratore__reparto='Uffici Sede')

    gruppi_lavoratori, n_gruppi_lavoratori = estrai_dati_util.dividi_elenco_lavoratori(lavoratori)

    context = {'titolo': 'Estrai Dati',
               'pagina_attiva_estrai_dati': 'active',
               'lavoratori': lavoratori,
               'n_gruppi_lavoratori': n_gruppi_lavoratori,
               'gruppi_lavoratori': gruppi_lavoratori,
               }

    return render(request, 'personale/estrai_dati.html', context)


def dati_estratti(request):
    if request.method == 'POST':

        lavoratori = []
        for x in request.POST.keys():
            if x != 'csrfmiddlewaretoken':
                lavoratore = Formazione.objects.get(id__exact=x)
                lavoratori.append(lavoratore)

        dati = estrai_dati_util.Estrai_Dati()
        dati.salva_lavoratori(lavoratori)

    context = {'titolo': 'Dati Estratti',
               'pagina_attiva_estrai_dati': 'active',
               'lavoratori': lavoratori,
               }

    return render(request, 'personale/dati_estratti.html', context)


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
    primo_soccorso_r = query.filter(primo_soccorso_ck='table-danger').count()
    primo_soccorso_g = query.filter(primo_soccorso_ck='table-warning').count()
    ponteggiatore_r = query.filter(ponteggiatore_ck='table-danger').count()
    ponteggiatore_g = query.filter(ponteggiatore_ck='table-warning').count()
    ept_r = query.filter(ept_ck='table-danger').count()
    ept_g = query.filter(ept_ck='table-warning').count()
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
        'primo_soccorso_r': primo_soccorso_r,
        'primo_soccorso_g': primo_soccorso_g,
        'ponteggiatore_r': ponteggiatore_r,
        'ponteggiatore_g': ponteggiatore_g,
        'ept_r': ept_r,
        'ept_g': ept_g,
        'ple_r': ple_r,
        'ple_g': ple_g,
    }

    return conteggio

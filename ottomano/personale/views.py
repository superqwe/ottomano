import datetime
import glob
import os

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
# import personale.importa_dati
from django.core.exceptions import ObjectDoesNotExist
from personale.models import Lavoratore, Formazione, Idoneita

from pprint import pprint as pp

from personale import aggiorna_documenti_util

PATH_DOCUMENTI = r'C:\Users\benedetto.basile\Dropbox\Documenti_Lavoratori'
# PATH_DOCUMENTI = r'z:\Documenti_Lavoratori'
OGGI = datetime.date.today()
FRA_N_MESI = OGGI + datetime.timedelta(days=30.5 * 12)
FRA_1_MESI = OGGI + datetime.timedelta(days=30.5)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# def importa_Personale_abilitazioni(request):
#     personale.importa_dati.importa_xlsx()
#     return HttpResponse("xls importato")

def anagrafica(request):
    lavoratori = Lavoratore.objects.filter(in_forza=True)
    context = {'titolo': 'Anagrafica',
               'pagina_attiva_anagrafica': 'active',
               'lavoratori': lavoratori}

    return render(request, 'personale/base.html', context)


def formazione(request):
    formazione = Formazione.objects.filter(lavoratore__in_forza=True)
    # print(formazione)
    context = {'titolo': 'Formazione',
               'pagina_attiva_formazione': 'active',
               'formazione': formazione}

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
            else:
                continue

        # ricerca attestati
        path_attestati = os.path.join(PATH_DOCUMENTI, lavoratore, 'attestati')
        try:
            attestati = os.listdir(path_attestati)
            attestati = aggiorna_documenti_util.calcola_data_attestati(attestati, lavoratore)
        except FileNotFoundError:
            attestati = []

        # lista_documenti.append([lavoratore, attestati])

        # salva su db
        if attestati or True:
            cognome, nome = lavoratore.split(maxsplit=1)

            try:
                formazione_ = Formazione.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)
                # print('----->', formazione_)
            except ObjectDoesNotExist:
                lavoratore = Lavoratore.objects.get(cognome__iexact=cognome, nome__iexact=nome)
                formazione_ = Formazione(lavoratore=lavoratore)

            for corso, data in attestati:
                setattr(formazione_, corso, data)

            formazione_.save()

        # ricerca idoneità
        path_lavoratore = os.path.join(PATH_DOCUMENTI, lavoratore)
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

                attestati.append(('idoneità', scadenza_idoneita))

            case 0:
                print('*** manca idoneità *** %s' % lavoratore)
            case _:
                print('*** più di una idoneità *** %s' % lavoratore)

        idoneita.save()

        ###
        lista_documenti.append([lavoratore, attestati])

    # pp(lista_documenti)

    os.chdir(PATH_DOCUMENTI)

    context = {'titolo': 'Aggiorna Documenti',
               'pagina_attiva_aggiorna_documenti': 'active',
               'lista_documenti': lista_documenti}

    return render(request, 'personale/aggiorna_documenti.html', context)


def aggiorna_stato(request):
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

    Formazione.objects.filter(preposto__lt=FRA_N_MESI).update(preposto_ck='table-warning')
    Formazione.objects.filter(primo_soccorso__lt=FRA_N_MESI).update(primo_soccorso_ck='table-warning')
    Formazione.objects.filter(antincendio__lt=FRA_N_MESI).update(antincendio_ck='table-warning')
    Formazione.objects.filter(art37__lt=FRA_N_MESI).update(art37_ck='table-warning')
    Formazione.objects.filter(spazi_confinati__lt=FRA_N_MESI).update(spazi_confinati_ck='table-warning')
    Formazione.objects.filter(ponteggiatore__lt=FRA_N_MESI).update(ponteggiatore_ck='table-warning')
    Formazione.objects.filter(imbracatore__lt=FRA_N_MESI).update(imbracatore_ck='table-warning')
    Formazione.objects.filter(ept__lt=FRA_N_MESI).update(ept_ck='table-warning')
    Formazione.objects.filter(autogru__lt=FRA_N_MESI).update(autogru_ck='table-warning')
    Formazione.objects.filter(gru_autocarro__lt=FRA_N_MESI).update(gru_autocarro_ck='table-warning')
    Formazione.objects.filter(carrello__lt=FRA_N_MESI).update(carrello_ck='table-warning')
    Formazione.objects.filter(sollevatore__lt=FRA_N_MESI).update(sollevatore_ck='table-warning')
    Formazione.objects.filter(ple__lt=FRA_N_MESI).update(ple_ck='table-warning')
    Formazione.objects.filter(rls__lt=FRA_N_MESI).update(rls_ck='table-warning')

    Formazione.objects.filter(preposto__lt=OGGI).update(preposto_ck='table-danger')
    Formazione.objects.filter(primo_soccorso__lt=OGGI).update(primo_soccorso_ck='table-danger')
    Formazione.objects.filter(antincendio__lt=OGGI).update(antincendio_ck='table-danger')
    Formazione.objects.filter(art37__lt=OGGI).update(art37_ck='table-danger')
    Formazione.objects.filter(spazi_confinati__lt=OGGI).update(spazi_confinati_ck='table-danger')
    Formazione.objects.filter(ponteggiatore__lt=OGGI).update(ponteggiatore_ck='table-danger')
    Formazione.objects.filter(imbracatore__lt=OGGI).update(imbracatore_ck='table-danger')
    Formazione.objects.filter(ept__lt=OGGI).update(ept_ck='table-danger')
    Formazione.objects.filter(autogru__lt=OGGI).update(autogru_ck='table-danger')
    Formazione.objects.filter(gru_autocarro__lt=OGGI).update(gru_autocarro_ck='table-danger')
    Formazione.objects.filter(carrello__lt=OGGI).update(carrello_ck='table-danger')
    Formazione.objects.filter(ple__lt=OGGI).update(ple_ck='table-danger')
    Formazione.objects.filter(rls__lt=OGGI).update(rls_ck='table-danger')
    # Formazione.objects.filter(__lt=OGGI).update(_ck='table-danger')
    # result.update(primo_soccorso_ck='table-warning')

    Idoneita.objects.filter(idoneita__gt=OGGI).update(idoneita_ck='')
    Idoneita.objects.filter(idoneita__lt=FRA_1_MESI).update(idoneita_ck='table-warning')
    Idoneita.objects.filter(idoneita=None).update(idoneita_ck='table-danger')
    Idoneita.objects.filter(idoneita__lte=OGGI).update(idoneita_ck='table-danger')

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

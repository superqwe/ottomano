import inspect
import pathlib
import datetime
from pprint import pp

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from personale.models import Lavoratore
from .models import Formazione, Non_Conformita, DPI2, CassettaPS, VerificaCassettaPS, RilevatoreH2S

import sgi.cassetta_ps_util as cassetta_ps_util
import sgi.scadenzario_dpi_util as scadenzario_dpi_util

PATH_DOCUMENTI = pathlib.Path(r'C:\Users\L. MASI\Documents\Documenti_Lavoratori')
FORMAZIONE_ANNO = 2024
FORMAZIONE_FRAZIONI_ORE = {
    '10min': 1 / 6,
    '15min': 0.25,
    '30min': 0.5,
    '1.5': 1.5,
    '1,5': 1.5,
}

OGGI = datetime.date.today()
FRA_4_MESI = OGGI + datetime.timedelta(days=30.5 * 6)


def index(request):
    return HttpResponse("Hello, world. You're at the personale index.")


def formazione(request, anno=FORMAZIONE_ANNO):
    formazione_ = Formazione.objects.filter(data__year=anno)

    # sessioni
    corsi_totali = formazione_.count()
    corsi_esterni = formazione_.filter(corso=None).count()
    corsi_interni = corsi_totali - corsi_esterni

    # ore
    ore_interno = ore_esterno = 0
    for corso in formazione_:
        if corso.ore.isnumeric():
            ore = int(corso.ore) * int(corso.persone)
        else:
            ore = FORMAZIONE_FRAZIONI_ORE[corso.ore] * int(corso.persone)

        if corso.corso:
            ore_interno += ore
        else:
            ore_esterno += ore

    ore_totali = ore_interno + ore_esterno

    # ore media persona
    n_lavoratori = Lavoratore.objects.filter(in_forza=True).count()
    media_interna = ore_interno / n_lavoratori
    media_esterna = ore_esterno / n_lavoratori
    media_totale = ore_totali / n_lavoratori

    # statistiche ore
    statistiche = (
        ('Corsi interni', corsi_interni, ore_interno, media_interna),
        ('Corsi esterni', corsi_esterni, ore_esterno, media_esterna),
        ('Totale', corsi_totali, ore_totali, media_totale)
    )

    context = {'titolo': 'Programma di informazione, formazione, addestramento',
               'pagina_attiva_formazione': 'active',
               'sezione_sgi_attiva': 'active',
               'formazione': formazione_,
               'statistiche': statistiche
               }

    pagina_attiva_formazione_2024 = pagina_attiva_formazione_2023 = pagina_attiva_formazione_2022 = ''

    match anno:
        case 2024:
            pagina_attiva_formazione_2024 = 'active'
        case 2023:
            pagina_attiva_formazione_2023 = 'active'
        case 2022:
            pagina_attiva_formazione_2022 = 'active'

    context['pagina_attiva_formazione_2024'] = pagina_attiva_formazione_2024
    context['pagina_attiva_formazione_2023'] = pagina_attiva_formazione_2023
    context['pagina_attiva_formazione_2022'] = pagina_attiva_formazione_2022

    return render(request, 'sgi/formazione.html', context)


def non_conformita(request, anno=FORMAZIONE_ANNO):
    non_conformita_ = Non_Conformita.objects.filter(data__year=anno).order_by('-data')

    context = {'titolo': 'Registro Non Conformità',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_nc': 'active',
               'elenco_non_conformita': non_conformita_,
               }

    pagina_attiva_non_conformita_2024 = pagina_attiva_non_conformita_2023 = ''

    match anno:
        case 2024:
            pagina_attiva_non_conformita_2024 = 'active'
        case 2023:
            pagina_attiva_non_conformita_2023 = 'active'

    context['pagina_attiva_non_conformita_2024'] = pagina_attiva_non_conformita_2024
    context['pagina_attiva_non_conformita_2023'] = pagina_attiva_non_conformita_2023

    return render(request, 'sgi/non_conformita.html', context)


def scadenzario_dpi_aggiorna(request):
    lavoratori = Lavoratore.objects.filter(in_forza=True)

    for lavoratore in lavoratori:
        cognome, nome = lavoratore.cognome, lavoratore.nome
        path_lavoratore = PATH_DOCUMENTI.joinpath('{} {}'.format(cognome, nome))
        consegna_dpi = list(path_lavoratore.glob('consegna_dpi*'))

        try:
            dpi = DPI2.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)
        except ObjectDoesNotExist:
            lavoratore = Lavoratore.objects.get(cognome__iexact=cognome, nome__iexact=nome)
            dpi = DPI2(lavoratore=lavoratore)

        if consegna_dpi:
            data_consegna = consegna_dpi[0].name.split()[1].split('.')[0]
            data_consegna = datetime.datetime.strptime(data_consegna, '%d%m%y')
            dpi.consegna = data_consegna

        dpi.save()

    # aggiorna data scadenza elemetto
    lista_dpi = DPI2.objects.filter(lavoratore__in_forza=True).exclude(lavoratore__cantiere__cantiere='Uffici Sede')

    for dpi in lista_dpi:
        data_fabbrica = dpi.elmetto_df

        if data_fabbrica:
            dpi.elmetto = datetime.datetime(data_fabbrica.year + 5, data_fabbrica.month, data_fabbrica.day)
            dpi.save()

    # aggiorna data scadenza rilevatore h2s
    lista_rilevatorih2s = RilevatoreH2S.objects.all()

    for rilevatore in lista_rilevatorih2s:
        try:
            dpi = DPI2.objects.get(lavoratore=rilevatore.lavoratore)
            dpi.rilevatore = rilevatore.data_scadenza
            dpi.save()
        except ObjectDoesNotExist:
            pass

    scadenzario_dpi_util.aggiorna_stato()

    return redirect(scadenzario_dpi)


def scadenzario_dpi_aggiorna_stato():
    pass


def scadenzario_dpi(request):
    lista_dpi = DPI2.objects.filter(lavoratore__in_forza=True).exclude(lavoratore__cantiere__cantiere='Uffici Sede')
    lista_rilevatorih2s = RilevatoreH2S.objects.all().exclude(uso='l')

    context = {'titolo': 'Scadenzario DPI',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_scadenzario_dpi': 'active',
               'lista_dpi': lista_dpi,
               'lista_rilevatorih2s': lista_rilevatorih2s,
               }

    return render(request, 'sgi/scadenzario_dpi.html', context)


def cassette_ps(request):
    CassettaPS.objects.all().update(ck_scadenza='ok_np')
    CassettaPS.objects.filter(scadenza__lt=FRA_4_MESI).update(ck_scadenza='table-warning')
    CassettaPS.objects.filter(scadenza__lt=OGGI).update(ck_scadenza='table-danger')

    lista_cassette = CassettaPS.objects.all()

    dati = []
    articoli_reintegro = {}
    for cassetta in lista_cassette:
        ultima_verifica = VerificaCassettaPS.objects.filter(cassetta=cassetta).select_related('cassetta')[0]
        cassetta.ultima_verifica = ultima_verifica.data_verifica
        cassetta.scadenza = ultima_verifica.data_scadenza

        match ultima_verifica.operazione:
            case 'ok' | 'rei':
                cassetta.stato = '1'
            case 'no':
                cassetta.stato = '-1'
                cassetta.ubicazione = 'Da reintegrare'
                for rigo in ultima_verifica.materiale_da_integrare.split('\n'):
                    n, articolo = rigo.split(' ', 1)
                    n = int(n[-1])
                    articolo = articolo.strip()
                    articoli_reintegro[articolo] = articoli_reintegro.get(articolo, 0) + n
            case 'dis':
                cassetta.stato = '0'
                cassetta.ubicazione = 'Dismessa'

        cassetta.save()
        dati.append((cassetta, ultima_verifica))

    articoli_reintegro = dict(sorted(articoli_reintegro.items()))

    context = {'titolo': 'Registro Cassette PS',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_cassette_ps': 'active',
               'pagina_attiva_cassette_ps_registro': 'active',
               'lista_cassette': dati,
               'articoli_reintegro': articoli_reintegro,
               }

    return render(request, 'sgi/cassette_ps.html', context)


def cassette_ps_storico(request):
    dati = VerificaCassettaPS.objects.all().order_by('-data_verifica')

    context = {'titolo': 'Storico verifiche Cassette PS',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_cassette_ps': 'active',
               'pagina_attiva_cassette_ps_storico': 'active',
               'lista_verifiche': dati,
               }
    return render(request, 'sgi/cassette_ps_storico.html', context)


def cassette_ps_scadenze(request):
    lista_cassette = CassettaPS.objects.exclude(stato='0')

    dati_cassette = []
    elenco_scadenze = []
    for cassetta in lista_cassette:
        verifica = VerificaCassettaPS.objects.filter(cassetta=cassetta).order_by('-data_verifica')[0]
        dati_cassette.append((cassetta, verifica))
        elenco_scadenze.append(verifica)

    n_cassette_per_rigo = 3
    dati_cassette = [dati_cassette[i: i + n_cassette_per_rigo] for i in
                     range(0, len(dati_cassette), n_cassette_per_rigo)]

    cassettaPS_Util = cassetta_ps_util.Cassetta_PS_Util(elenco_scadenze)
    prodotti_in_scadenza_all1, prodotti_in_scadenza_all2 = cassettaPS_Util.prodotti_in_scadenza()

    context = {'titolo': 'Scadenze Cassette PS',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_cassette_ps': 'active',
               'pagina_attiva_cassette_ps_scadenze': 'active',
               'gruppi_cassetta': dati_cassette,
               'prodotti_in_scadenza_all1': prodotti_in_scadenza_all1,
               'prodotti_in_scadenza_all2': prodotti_in_scadenza_all2,
               }

    return render(request, 'sgi/cassette_ps_scadenze.html', context)


def rilevatorih2s(request):
    dati = RilevatoreH2S.objects.all()

    context = {'titolo': 'Registro Rilevatori H2S',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_rilevatorih2s': 'active',
               'registro': dati,
               }

    return render(request, 'sgi/rilevatorih2s.html', context)

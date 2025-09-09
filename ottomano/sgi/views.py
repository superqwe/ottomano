import datetime
import pathlib

import sgi.cassetta_ps_util as cassetta_ps_util
import sgi.formazione_cantieri_util as formazione_cantieri_util
import sgi.rilevatorih2s_util as rilevatorih2s_util
import sgi.scadenzario_dpi_util as scadenzario_dpi_util
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from icecream import ic
from personale.models import Lavoratore

from .models import AccessoriSollevamento, AccessoriSollevamento_Revisione, CassettaPS, DPI2, DPI_Anticaduta2, \
    DPI_Anticaduta_Operazione, Formazione, Formazione_Organico_Medio_Annuo, NearMiss, Non_Conformita, \
    RilevatoreH2S, \
    VerificaCassettaPS
from .models import DPI_ANTICADUTA_TIPOLOGIA

if settings.NOME_COMPUTER.lower() == 'srvdc1':
    PATH_DOCUMENTI = pathlib.Path(r'D:\Gestionale\Documenti_Lavoratori')
else:
    PATH_DOCUMENTI = pathlib.Path(r'C:\Users\L. MASI\Documents\Documenti_Lavoratori')
ANNO_CORRENTE = datetime.date.today().year
FORMAZIONE_FRAZIONI_ORE = {
    '10min': 1 / 6,
    '15min': 0.25,
    '30min': 0.5,
    '1.5': 1.5,
    '1,5': 1.5,
}

OGGI = datetime.date.today()
FRA_4_MESI = OGGI + datetime.timedelta(days=30.5 * 6)
DA_3_MESI = OGGI - datetime.timedelta(days=30.5 * 3)
DA_6_MESI = OGGI - datetime.timedelta(days=30.5 * 6)
DA_9_MESI = OGGI - datetime.timedelta(days=30.5 * 9)
DA_12_MESI = OGGI - datetime.timedelta(days=30.5 * 12)
DA_18_MESI = OGGI - datetime.timedelta(days=30.5 * 18)


def test(request):
    a = DPI_Anticaduta_Operazione.objects.all().order_by('data', 'operazione', 'lavoratore')
    ic(a)

    operazioni = DPI_Anticaduta_Operazione.objects.all().order_by('data', 'operazione', 'lavoratore')

    b = [(x.data, x.operazione, x.lavoratore) for x in operazioni]

    duplicati = []
    for x in b:
        q = DPI_Anticaduta_Operazione.objects.filter(data=x[0], operazione=x[1], lavoratore=x[2])
        if len(q) > 1:
            ic(x, len(q))
            duplicati.append(x)

    ic(set(duplicati))

    # op = operazioni[0].dpi_anticaduta2_set.all()
    # opd = dir(op)

    context = {
        'a': a,

    }

    # per visualizzare operazioni senza associazione ##########################
    # for operazione in operazioni:
    #     x = operazione.dpi_anticaduta2_set.all()
    #     if not x:
    #         print(operazione.data, operazione.lavoratore, operazione.pk)
    #         print(operazione.dpi_anticaduta2_set.all())
    #         print()
    ###########################################################################

    return render(request, 'sgi/test.html', context)


def index(request):
    return HttpResponse("Hello, world. You're at the personale index.")


def formazione(request, anno_attivo=ANNO_CORRENTE):
    formazione_ = Formazione.objects.filter(data__year=anno_attivo)

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
    try:
        organico_medio_annuo = Formazione_Organico_Medio_Annuo.objects.get(anno=anno_attivo).valore
    except ObjectDoesNotExist:
        organico_medio_annuo = Lavoratore.objects.filter(in_forza=True).count()

    media_interna = ore_interno / organico_medio_annuo
    media_esterna = ore_esterno / organico_medio_annuo
    media_totale = ore_totali / organico_medio_annuo

    # statistiche ore
    statistiche = (
        ('Corsi interni', corsi_interni, ore_interno, media_interna),
        ('Corsi esterni', corsi_esterni, ore_esterno, media_esterna),
        ('Totale', corsi_totali, ore_totali, media_totale)
    )

    # menu anni
    anni = Formazione.objects.dates('data', 'year', order='DESC')
    anni = [x.year for x in anni]

    if ANNO_CORRENTE not in anni:
        anni.insert(0, ANNO_CORRENTE)

    menu_anni = []

    for anno in anni:
        attivo = 'active' if anno_attivo == anno else ''
        menu_anni.append((anno, attivo))

    context = {'titolo': 'Programma di informazione, formazione, addestramento',
               'pagina_attiva_formazione': 'active',
               'sezione_sgi_attiva': 'active',
               'formazione': formazione_,
               'statistiche': statistiche,
               'organico_medio_annuo': organico_medio_annuo,
               'menu_anni': menu_anni,
               }

    return render(request, 'sgi/formazione.html', context)


def non_conformita(request, anno=ANNO_CORRENTE):
    non_conformita_ = Non_Conformita.objects.filter(data__year=anno).order_by('-data')

    # menu anni
    anni = Non_Conformita.objects.dates('data', 'year', order='DESC')
    anni = [x.year for x in anni]

    if ANNO_CORRENTE not in anni:
        anni.insert(0, ANNO_CORRENTE)

    menu_anni = []

    for anno_ in anni:
        attivo = 'active' if anno == anno_ else ''
        menu_anni.append((anno_, attivo))

    context = {'titolo': 'Registro Non Conformità',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_nc': 'active',
               'elenco_non_conformita': non_conformita_,
               'menu_anni': menu_anni,
               }

    return render(request, 'sgi/non_conformita.html', context)


def near_miss(request, anno=ANNO_CORRENTE):
    near_miss_ = NearMiss.objects.filter(data__year=anno).order_by('-data')

    # menu anni
    anni = NearMiss.objects.dates('data', 'year', order='DESC')
    anni = [x.year for x in anni]

    if ANNO_CORRENTE not in anni:
        anni.insert(0, ANNO_CORRENTE)

    menu_anni = []

    for anno_ in anni:
        attivo = 'active' if anno == anno_ else ''
        menu_anni.append((anno_, attivo))

    context = {'titolo': 'Near Miss/Medicazioni',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_near_miss': 'active',
               'elenco_near_miss': near_miss_,
               'menu_anni': menu_anni,
               }

    # pagina_attiva_near_miss_2025 = pagina_attiva_near_miss_2024 = pagina_attiva_near_miss_2023 = ''
    #
    # match anno:
    #     case 2025:
    #         pagina_attiva_near_miss_2025 = 'active'
    #     case 2024:
    #         pagina_attiva_near_miss_2024 = 'active'
    #     case 2023:
    #         pagina_attiva_near_miss_2023 = 'active'
    #
    # context['pagina_attiva_near_miss_2025'] = pagina_attiva_near_miss_2025
    # context['pagina_attiva_near_miss_2024'] = pagina_attiva_near_miss_2024
    # context['pagina_attiva_near_miss_2023'] = pagina_attiva_near_miss_2023

    return render(request, 'sgi/near_miss.html', context)


# # todo: obsoleto
# def scadenzario_dpi_aggiorna(request):
#
#     lavoratori = Lavoratore.objects.filter(in_forza=True)
#
#     for lavoratore in lavoratori:
#         cognome, nome = lavoratore.cognome, lavoratore.nome
#         path_lavoratore = PATH_DOCUMENTI.joinpath('{} {}'.format(cognome, nome))
#         consegna_dpi = list(path_lavoratore.glob('consegna_dpi*'))
#
#         try:
#             dpi = DPI2.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)
#         except ObjectDoesNotExist:
#             lavoratore = Lavoratore.objects.get(cognome__iexact=cognome, nome__iexact=nome)
#             dpi = DPI2(lavoratore=lavoratore)
#
#         if consegna_dpi:
#             data_consegna = consegna_dpi[0].name.split()[1].split('.')[0]
#             data_consegna = datetime.datetime.strptime(data_consegna, '%d%m%y')
#             dpi.consegna = data_consegna
#
#         dpi.save()
#
#     # aggiorna data scadenza elemetto
#     lista_dpi = DPI2.objects.filter(lavoratore__in_forza=True).exclude(lavoratore__cantiere__cantiere='Uffici Sede')
#
#     for dpi in lista_dpi:
#         data_fabbrica = dpi.elmetto_df
#
#         if data_fabbrica:
#             dpi.elmetto = datetime.datetime(data_fabbrica.year + 5, data_fabbrica.month, data_fabbrica.day)
#             dpi.save()
#
#     # aggiorna data scadenza rilevatore h2s
#     lista_rilevatorih2s = RilevatoreH2S.objects.exclude(uso='x')
#
#     for rilevatore in lista_rilevatorih2s:
#         try:
#             dpi = DPI2.objects.get(lavoratore=rilevatore.lavoratore)
#             dpi.rilevatore = rilevatore.data_scadenza
#             dpi.ck_rilevatore_calibrazione = rilevatore.data_calibrazione_ck
#             dpi.save()
#         except ObjectDoesNotExist:
#             pass
#
#     scadenzario_dpi_util.aggiorna_stato()
#
#     scadenzario_dpi_util.aggiorna_dpi_anticaduta()
#
#     return redirect(scadenzario_dpi)


def scadenzario_dpi_aggiorna2(request):
    lavoratori = Lavoratore.objects.filter(in_forza=True).select_related('cantiere')
    dpi_map = {
        (dpi.lavoratore.cognome.lower(), getattr(dpi.lavoratore, 'nome', '').lower()): dpi
        for dpi in DPI2.objects.select_related('lavoratore').all()
    }

    # aggiorna_consegna_dpi
    updated_dpi = []

    for lavoratore in lavoratori:
        # print(lavoratore)
        cognome = lavoratore.cognome
        nome = getattr(lavoratore, 'nome', '')
        path_lavoratore = PATH_DOCUMENTI.joinpath(f'{cognome} {nome}')
        consegna_dpi_files = list(path_lavoratore.glob('consegna_dpi*'))
        # print(consegna_dpi_files)
        # print('-')

        dpi = dpi_map.get((cognome.lower(), nome.lower()))
        if not dpi:
            dpi = DPI2(lavoratore=lavoratore)

        if consegna_dpi_files:
            try:
                data_str = consegna_dpi_files[0].name.split()[1].split('.')[0]
                data_consegna = datetime.datetime.strptime(data_str, '%d%m%y')
                dpi.consegna = data_consegna
                updated_dpi.append(dpi)
            except (IndexError, ValueError):
                continue

    DPI2.objects.bulk_update(updated_dpi, ['consegna'])

    # aggiorna data scadenza elemetto
    lista_dpi = DPI2.objects.filter(
        lavoratore__in_forza=True
    ).exclude(
        lavoratore__cantiere__cantiere='Uffici Sede'
    ).select_related('lavoratore', 'lavoratore__cantiere')

    updated_dpi = []

    for dpi in lista_dpi:
        if dpi.elmetto_df:
            try:
                scadenza = datetime.datetime(dpi.elmetto_df.year + 5, dpi.elmetto_df.month,
                                             dpi.elmetto_df.day)
                dpi.elmetto = scadenza
                updated_dpi.append(dpi)
            except ValueError:
                continue

    DPI2.objects.bulk_update(updated_dpi, ['elmetto'])

    # aggiorna data scadenza rilevatore h2s
    rilevatori = RilevatoreH2S.objects.exclude(uso='x').select_related('lavoratore')
    updated_dpi = []

    for rilevatore in rilevatori:
        try:
            dpi = DPI2.objects.get(lavoratore=rilevatore.lavoratore)
            dpi.rilevatore = rilevatore.data_scadenza
            # Se esiste il campo ck_rilevatore_calibrazione:
            # dpi.ck_rilevatore_calibrazione = rilevatore.data_calibrazione_ck
            updated_dpi.append(dpi)
            # print(rilevatore.lavoratore, rilevatore.data_calibrazione)
        except DPI2.DoesNotExist:
            continue

    scadenzario_dpi_util.aggiorna_stato2()

    scadenzario_dpi_util.aggiorna_dpi_anticaduta2()

    return redirect(scadenzario_dpi)


def scadenzario_dpi(request):
    lista_dpi = DPI2.objects.filter(lavoratore__in_forza=True).exclude(
        lavoratore__cantiere__cantiere='Uffici Sede')
    lista_rilevatorih2s = RilevatoreH2S.objects.exclude(uso='l').exclude(uso='x')

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

    CassettaPS.objects.all().update(ck_ultima_verifica='ok_np')
    CassettaPS.objects.filter(ultima_verifica__lt=DA_6_MESI).update(ck_ultima_verifica='table-warning')
    CassettaPS.objects.filter(ultima_verifica__lt=DA_9_MESI).update(ck_ultima_verifica='table-danger')

    lista_cassette = CassettaPS.objects.exclude(Q(stato=0) & Q(ultima_verifica__lt=DA_6_MESI))

    dati = []
    articoli_reintegro = {}
    for cassetta in lista_cassette:
        try:
            ultima_verifica = VerificaCassettaPS.objects.filter(cassetta=cassetta).select_related('cassetta')[
                0]
            cassetta.ultima_verifica = ultima_verifica.data_verifica
            cassetta.scadenza = ultima_verifica.data_scadenza

            match ultima_verifica.operazione:
                case 'ok' | 'rei':
                    cassetta.stato = '1'
                case 'no':
                    cassetta.stato = '-1'
                    cassetta.ubicazione = 'Da reintegrare'
                    for rigo in ultima_verifica.materiale_da_integrare.split('\n'):
                        try:
                            n, articolo = rigo.split(' ', 1)
                            n = int(n[-1])
                            articolo = articolo.strip()
                            articoli_reintegro[articolo] = articoli_reintegro.get(articolo, 0) + n
                        except ValueError:
                            print('--> ERRORE -->', cassetta, rigo, '<---')
                case 'dis':
                    cassetta.stato = '0'
                    cassetta.ubicazione = 'Dismessa'

        except IndexError:
            ultima_verifica = None

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


def cassette_ps_aggiungi_verifica(request, n_cassetta):
    cassetta = CassettaPS.objects.get(pk=n_cassetta)

    verifiche = VerificaCassettaPS.objects.filter(cassetta=cassetta).select_related('cassetta').order_by(
        '-data_verifica')

    if verifiche:
        ultima_verifica = verifiche[0]
        ultima_verifica.pk = None
        ultima_verifica.data_verifica = datetime.date.today()
        ultima_verifica.save()

        return redirect(f'/admin/sgi/verificacassettaps/{ultima_verifica.pk}/')

    else:
        return redirect('/admin/sgi/verificacassettaps/add/')


def cassette_ps_storico(request, anno=ANNO_CORRENTE):
    dati = VerificaCassettaPS.objects.filter(data_verifica__year=anno).order_by('-data_verifica', 'cassetta')

    materiale_integrato_1 = {}
    materiale_integrato_2 = {}
    for verifica in dati:
        allegato = verifica.cassetta.allegato
        materiale_integrato_verifica = [
            (int(x.strip().split(' ', 1)[0].split('.')[1]), x.strip().split(' ', 1)[1]) for
            x in verifica.materiale_integrato.split('\n') if x]

        for n, articolo in materiale_integrato_verifica:

            if allegato == '1':
                materiale_integrato_1[articolo] = materiale_integrato_1.get(articolo, 0) + n
            elif allegato == '2':
                materiale_integrato_2[articolo] = materiale_integrato_2.get(articolo, 0) + n

    materiale_integrato_1 = dict(sorted(materiale_integrato_1.items()))
    materiale_integrato_2 = dict(sorted(materiale_integrato_2.items()))

    anni = VerificaCassettaPS.objects.dates('data_verifica', 'year', order='DESC')
    anni = [x.year for x in anni]

    if ANNO_CORRENTE not in anni:
        anni.insert(0, ANNO_CORRENTE)

    menu_anni = []

    for anno_ in anni:
        attivo = 'active' if anno == anno_ else ''
        menu_anni.append((anno_, attivo))

    context = {'titolo': 'Storico verifiche Cassette PS',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_cassette_ps': 'active',
               'pagina_attiva_cassette_ps_storico': 'active',
               'lista_verifiche': dati,
               'materiale_integrato_1': materiale_integrato_1,
               'materiale_integrato_2': materiale_integrato_2,
               'menu_anni': menu_anni,
               }

    # context['pagina_attiva_cassette_ps_storico_%i' % anno] = 'active'

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
    # ic(dati_cassette)

    # cassettaPS_Util = cassetta_ps_util.Cassetta_PS_Util(elenco_scadenze)
    cassettaPS_Util = cassetta_ps_util.Cassetta_PS_Util2(elenco_scadenze)
    prodotti_in_scadenza_all1, prodotti_in_scadenza_all2 = cassettaPS_Util.aggiorna_stato_scadenza()

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
    rilevatorih2s_util.rilevatori_drager_calibrazione_stato()
    dati = RilevatoreH2S.objects.exclude(data_scadenza__lt=DA_6_MESI)

    context = {'titolo': 'Registro Rilevatori H2S',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_rilevatorih2s': 'active',
               'registro': dati,
               }

    return render(request, 'sgi/rilevatorih2s.html', context)


def accessori_sollevamento(request):
    AccessoriSollevamento.objects.filter(in_uso=True).update(stato='ok')
    AccessoriSollevamento.objects.filter(data_messa_in_servizio__gt=DA_6_MESI).update(stato='recente')
    AccessoriSollevamento.objects.filter(in_uso=False).update(stato='dismessa')
    AccessoriSollevamento.objects.filter(data_dismissione__gt=DA_6_MESI).update(stato='dismessa_recente')

    # AccessoriSollevamento.objects.filter(usura_leggera=True).update(usura='1')
    # AccessoriSollevamento.objects.filter(usura_media=True).update(usura='2')
    # AccessoriSollevamento.objects.filter(usura_grave=True).update(usura='3')

    dati = AccessoriSollevamento.objects.exclude(stato='dismessa')

    revisione = AccessoriSollevamento_Revisione.objects.all()[0]

    context = {'titolo': 'Registro Accessori di Sollevamento',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_accessori_sollevamento': 'active',
               'registro': dati,
               'revisione': revisione,
               }
    return render(request, 'sgi/accessori_sollevamento.html', context)


def dpi_anticaduta_registro(request):
    # dati = DPI_Anticaduta2.objects.all()
    # [x.save() for x in dati]  # forza salvataggio

    dati = DPI_Anticaduta2.objects.exclude(stato__in=('x', 'v', 'vi', 'vd')).order_by('lavoratore')
    registro = {}
    disponibili = []

    for dpi in dati:

        if dpi.lavoratore:

            if dpi.lavoratore not in registro:
                registro[dpi.lavoratore] = [None, ] * 3

            match dpi.tipologia:
                case 'im':
                    registro[dpi.lavoratore][0] = dpi
                case 'c1':
                    registro[dpi.lavoratore][1] = dpi
                case 'c2':
                    registro[dpi.lavoratore][2] = dpi
        else:
            disponibili.append(dpi)

    dati = []
    for lavoratore, dpi in registro.items():
        dati.append((lavoratore, dpi))

    disponibili_imbracature = DPI_Anticaduta2.objects.filter(stato='d').filter(tipologia='im')
    disponibili_cordino_singolo = DPI_Anticaduta2.objects.filter(stato='d').filter(tipologia='c1')
    disponibili_cordino_doppio = DPI_Anticaduta2.objects.filter(stato='d').filter(tipologia='c2')
    retrattili = DPI_Anticaduta2.objects.filter(tipologia='rt')

    in_verifica = ['v', 'vi', 'vd']
    verifica_imbracature = DPI_Anticaduta2.objects.filter(stato__in=in_verifica).filter(tipologia='im')
    verifica_cordino_singolo = DPI_Anticaduta2.objects.filter(stato__in=in_verifica).filter(tipologia='c1')
    verifica_cordino_doppio = DPI_Anticaduta2.objects.filter(stato__in=in_verifica).filter(tipologia='c2')

    dismessi_imbracature = DPI_Anticaduta2.objects. \
        filter(stato='x').filter(tipologia='im'). \
        exclude(dismissione__lt=DA_6_MESI)
    dismessi_cordino_singolo = DPI_Anticaduta2.objects. \
        filter(stato='x').filter(tipologia='c1'). \
        exclude(dismissione__lt=DA_6_MESI)
    dismessi_cordino_doppio = DPI_Anticaduta2.objects. \
        filter(stato='x').filter(tipologia='c2'). \
        exclude(dismissione__lt=DA_6_MESI)

    context = {'titolo': 'Registro DPI Anticaduta',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_dpi_anticaduta': 'active',
               'pagina_attiva_dpi_anticaduta_registro': 'active',
               'registro': dati,
               'dismessi_imbracature': dismessi_imbracature,
               'dismessi_cordino_singolo': dismessi_cordino_singolo,
               'dismessi_cordino_doppio': dismessi_cordino_doppio,
               'disponibili_imbracature': disponibili_imbracature,
               'disponibili_cordino_singolo': disponibili_cordino_singolo,
               'disponibili_cordino_doppio': disponibili_cordino_doppio,
               'retrattili': retrattili,
               'verifica_imbracature': verifica_imbracature,
               'verifica_cordino_singolo': verifica_cordino_singolo,
               'verifica_cordino_doppio': verifica_cordino_doppio,
               }
    return render(request, 'sgi/dpi_anticaduta_registro.html', context)


def dpi_anticaduta_elenco(request):
    # todo: da completare ck_revisione con più date di verifica
    DPI_Anticaduta2.objects.all().update(ck_revisione='ok_np')

    DPI_Anticaduta2.objects.filter(
        Q(data_verifica=None) & (Q(messa_in_servizio__lt=DA_9_MESI))
    ).update(ck_revisione='table-warning')

    DPI_Anticaduta2.objects.filter(Q(data_verifica__lt=DA_9_MESI)).update(ck_revisione='table-warning')

    DPI_Anticaduta2.objects.filter(
        Q(data_verifica=None) & (Q(messa_in_servizio__lt=DA_12_MESI) | Q(messa_in_servizio=None))
    ).update(ck_revisione='table-danger')

    DPI_Anticaduta2.objects.filter(Q(data_verifica__lt=DA_12_MESI)).update(ck_revisione='table-danger')

    DPI_Anticaduta2.objects.filter(
        Q(data_verifica=None) & (Q(messa_in_servizio=None))).update(ck_revisione='')

    dati = DPI_Anticaduta2.objects.exclude(dismissione__lt=DA_6_MESI)

    context = {'titolo': 'Elenco DPI Anticaduta',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_dpi_anticaduta': 'active',
               'pagina_attiva_dpi_anticaduta_elenco': 'active',
               'registro': dati,
               'tipologie': DPI_ANTICADUTA_TIPOLOGIA,
               }
    return render(request, 'sgi/dpi_anticaduta_elenco.html', context)


def dpi_anticaduta_storia(request):
    dati = DPI_Anticaduta2.objects.all().order_by('tipologia', 'matricola_interna')

    context = {'titolo': 'Storia DPI Anticaduta',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_dpi_anticaduta': 'active',
               'pagina_attiva_dpi_anticaduta_storia': 'active',
               'dati': dati,
               'tipologie': DPI_ANTICADUTA_TIPOLOGIA,
               }
    return render(request, 'sgi/dpi_anticaduta_storia.html', context)


def formazione_cantieri(request):
    intestazione = formazione_cantieri_util.IntestazioneTabella()

    context = {'titolo': 'Formazione Cantieri',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_formazione_cantieri': 'active',
               'rigo1': intestazione.rigo1,
               'rigo2': intestazione.rigo2,
               'rigo3': intestazione.rigo3,
               'dati': intestazione.dati,
               }
    return render(request, 'sgi/formazione_cantieri.html', context)

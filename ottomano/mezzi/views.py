import datetime
import os.path
import warnings
from pathlib import Path

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from icecream import ic
from mezzi import views_util
from mezzi.models import Mezzo, RCT

if settings.NOME_COMPUTER.lower() == 'srvdc1':
    PATH_DOCUMENTI = r'D:\Gestionale\Documenti_Mezzi'
else:
    PATH_DOCUMENTI = r'C:\Users\L. MASI\Documents\Documenti_Mezzi'

OGGI = datetime.date.today()
FRA_1_MESI = OGGI + datetime.timedelta(days=30.5)


def index(request):
    return HttpResponse("Hello, world. You're at the mezzi index.")


def elenco(request):
    mezzi = Mezzo.objects.filter(in_forza=True)
    context = {'titolo': 'Elenco Mezzi',
               'sezione_mezzi_attiva': 'active',
               'pagina_attiva_elenco': 'active',
               'mezzi': mezzi}

    return render(request, 'mezzi/elenco.html', context)


def scadenziario(request):
    mezzi = Mezzo.objects.filter(in_forza=True, stato__in=['giallo', 'rosso'])

    context = {'titolo': 'Elenco Mezzi',
               'sezione_mezzi_attiva': 'active',
               'pagina_attiva_scadenzario': 'active',
               'mezzi': mezzi}

    return render(request, 'mezzi/elenco.html', context)


def aggiorna_stato(request):
    Mezzo.objects.filter(in_forza=True).update(stato='verde')

    Mezzo.objects.filter(Q(assicurazione__gt=OGGI) | Q(assicurazione__isnull=True)).update(assicurazione_ck='')
    Mezzo.objects.filter(Q(revisione__gt=OGGI) | Q(revisione__isnull=True)).update(revisione_ck='')
    Mezzo.objects.filter(Q(inail__gt=OGGI) | Q(inail__isnull=True)).update(inail_ck='')

    Mezzo.objects.filter(assicurazione__lt=FRA_1_MESI).update(assicurazione_ck='table-warning', stato='giallo')
    Mezzo.objects.filter(revisione__lt=FRA_1_MESI).update(revisione_ck='table-warning', stato='giallo')
    Mezzo.objects.filter(inail__lt=FRA_1_MESI).update(inail_ck='table-warning', stato='giallo')

    Mezzo.objects.filter(assicurazione__lt=OGGI).update(assicurazione_ck='table-danger', stato='rosso')
    Mezzo.objects.filter(revisione__lt=OGGI).update(revisione_ck='table-danger', stato='rosso')
    Mezzo.objects.filter(inail__lt=OGGI).update(inail_ck='table-danger', stato='rosso')

    rct = RCT.objects.get().scadenza

    if rct <= FRA_1_MESI:
        colore = 'giallo'
    elif rct <= OGGI:
        colore = 'rosso'
    else:
        colore = 'verde'

    Mezzo.objects.filter(rct_aziendale=True).update(rct_aziendale_ck=colore, stato=colore)
    return redirect('/mezzi/elenco')


def aggiorna_documenti(request):
    elenco_mezzi = Mezzo.objects.all()

    elenco_documenti_mezzi = []
    for mezzo in elenco_mezzi:
        # print('\n', mezzo.nome())
        path_mezzo = os.path.join(PATH_DOCUMENTI, mezzo.nome())

        documenti = os.listdir(path_mezzo)

        documenti_mezzo_ok = []
        documenti_mezzo_errore = []
        for documento in documenti:
            documenti_mezzo_ok.append(os.path.splitext(documento)[0])
            doc = os.path.splitext(documento)[0].split()

            match doc[0]:
                case 'altro':
                    documenti_mezzo_errore.append((documenti_mezzo_ok.pop()))

                case 'assicurazione':
                    data = views_util.str2datetime(doc[1])
                    mezzo.assicurazione = data

                case 'ce':
                    mezzo.ce = True

                case 'ce_accessori':
                    mezzo.ce_accessori = True

                case 'immatricolazione':
                    data = views_util.str2datetime(doc[1])
                    mezzo.immatricolazione = data

                    if mezzo.inail is None:
                        data_inail = views_util.aggiungi_anni(data)
                        mezzo.inail = data_inail

                case 'libretto':
                    match len(doc):
                        case 2:
                            data = views_util.str2datetime(doc[1])
                            mezzo.revisione = data
                            mezzo.libretto = True
                        case 1:
                            mezzo.libretto = True
                        case _:
                            documenti_mezzo_errore.append((documenti_mezzo_ok.pop()))
                            warnings.warn('Nome file errato - %s' % documento)

                case 'libretto_inail':
                    mezzo.libretto_inail = True

                case 'manuale':
                    mezzo.manuale = True

                case 'verifica_periodica':
                    data = views_util.str2datetime(doc[1])
                    data_scadenza_verifica = views_util.aggiungi_anni(data)
                    mezzo.inail = data_scadenza_verifica

                case _:
                    documenti_mezzo_errore.append((documenti_mezzo_ok.pop()))
                    warnings.warn('Nome documento non processato - %s (%s)' % (mezzo, documento))

        mezzo.save()
        elenco_documenti_mezzi.append((mezzo, documenti_mezzo_ok, documenti_mezzo_errore))

    # data automatica RCT
    path_rct = Path(PATH_DOCUMENTI).glob('rct*')
    rct_scadenza = max([datetime.datetime.strptime(path.name.split()[1].split('.')[0], "%d%m%y") for path in path_rct])

    rct = RCT.objects.first()
    rct.scadenza = rct_scadenza
    rct.save()


    context = {'titolo': 'Documenti Mezzi Aggiornati',
               'sezione_mezzi_attiva': 'active',
               'pagina_attiva_aggiorna_documenti': 'active',
               'mezzi': elenco_documenti_mezzi,
               'rct': rct_scadenza,
               }

    return render(request, 'mezzi/aggiorna_documenti.html', context)

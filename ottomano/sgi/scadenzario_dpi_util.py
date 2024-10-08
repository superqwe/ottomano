import datetime
import inspect
from pprint import pp

from sgi.models import DPI2, DPI_Anticaduta2

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

OGGI = datetime.date.today()
FRA_3_MESI = OGGI + datetime.timedelta(days=30.5 * 3)
MESI_6_PASSATI = OGGI - datetime.timedelta(days=30.5 * 6)
MESI_9_PASSATI = OGGI - datetime.timedelta(days=30.5 * 9)


def aggiungi_n_anni(data, n=10):
    data_out = datetime.date(data.year + n, data.month, 1)
    return data_out


def aggiorna_stato():
    DPI2.objects.filter(Q(consegna__lte=OGGI)).update(ck_consegna=None)
    DPI2.objects.filter(Q(consegna__lt=MESI_6_PASSATI)).update(ck_consegna='table-warning')
    DPI2.objects.filter(Q(consegna__lt=MESI_9_PASSATI) | Q(consegna__isnull=True)).update(ck_consegna='table-danger')

    DPI2.objects.filter(Q(elmetto__gt=OGGI)).update(ck_elmetto='')
    DPI2.objects.filter(Q(elmetto__lt=FRA_3_MESI)).update(ck_elmetto='table-warning')
    DPI2.objects.filter(Q(elmetto__lt=OGGI) | Q(elmetto__isnull=True)).update(ck_elmetto='table-danger')

    DPI2.objects.filter(Q(rilevatore__gt=OGGI)).update(ck_rilevatore='')
    DPI2.objects.filter(Q(rilevatore__lt=FRA_3_MESI)).update(ck_rilevatore='table-warning')
    DPI2.objects.filter(Q(rilevatore__lt=OGGI) | Q(rilevatore__isnull=True)).update(ck_rilevatore='table-danger')

    DPI2.objects.filter(Q(maschera__gt=OGGI)).update(ck_maschera='')
    DPI2.objects.filter(Q(maschera__lt=FRA_3_MESI)).update(ck_maschera='table-warning')
    DPI2.objects.filter(Q(maschera__lt=OGGI) | Q(maschera__isnull=True)).update(ck_maschera='table-danger')


def aggiorna_dpi_anticaduta():
    anticaduta = DPI_Anticaduta2.objects.all().exclude(stato='x')

    for articolo in anticaduta:
        try:
            dpi = DPI2.objects.get(lavoratore=articolo.lavoratore)
            scadenza = aggiungi_n_anni(articolo.fabbricazione)

            match articolo.tipologia:
                case 'im':
                    dpi.imbracatura = scadenza

                case 'c1':
                    dpi.cordino_singolo = scadenza

                case 'c2':
                    dpi.cordino_doppio = scadenza

            dpi.save()

        except ObjectDoesNotExist:
            pass

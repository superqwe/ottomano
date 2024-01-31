import datetime
import inspect
from pprint import pp

from sgi.models import DPI2

from django.db.models import Q

OGGI = datetime.date.today()
FRA_3_MESI = OGGI + datetime.timedelta(days=30.5 * 3)
MESI_6_PASSATI = OGGI - datetime.timedelta(days=30.5 * 6)
MESI_9_PASSATI = OGGI - datetime.timedelta(days=30.5 * 9)


def aggiorna_stato():
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

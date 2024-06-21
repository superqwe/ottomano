import datetime

from sgi.models import RilevatoreH2S
from django.db.models import Q

from pprint import pprint as pp

OGGI = datetime.date.today()
FRA_3_MESI = OGGI + datetime.timedelta(days=30.5 * 3)
MESI_6_PASSATI = OGGI - datetime.timedelta(days=30.5 * 6)
MESI_9_PASSATI = OGGI - datetime.timedelta(days=30.5 * 9)
GIORNI_180_DA_ATTIVAZIONE = OGGI + datetime.timedelta(days=365 * 2 - 180)
GIORNI_180_DA_ATTIVAZIONE_IN_SCADENZA = OGGI + datetime.timedelta(days=365 * 2 - 180 - 30)


def rilevatori_drager_calibrazione_stato():
    # todo: implementare scadenza rilevatori già calibrati
    drager = RilevatoreH2S.objects.filter(marca='dr')

    drager.update(data_calibrazione_ck=None)

    prima_calibrazione_in_scadenza = drager. \
        filter(data_calibrazione=None). \
        filter(data_scadenza__lt=GIORNI_180_DA_ATTIVAZIONE_IN_SCADENZA). \
        update(data_calibrazione_ck='table-warning')
    prima_calibrazione_scaduti = drager. \
        filter(data_calibrazione=None). \
        filter(data_scadenza__lt=GIORNI_180_DA_ATTIVAZIONE). \
        update(data_calibrazione_ck='table-danger')

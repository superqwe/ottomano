import datetime
import inspect
from pprint import pprint as pp

OGGI = datetime.date.today()
FRA_4_MESI = OGGI + datetime.timedelta(days=30.5 * 6)


class Cassetta_PS_Util:
    def __init__(self, verifica):
        self.verifiche = verifica

    def prodotti_in_scadenza(self):
        prodotti_in_scadenza_all1 = []
        prodotti_in_scadenza_all2 = []
        for verifica in self.verifiche:

            for prodotto, scadenza in inspect.getmembers(verifica):

                match verifica.cassetta.allegato:
                    case '1':
                        try:
                            if prodotto.startswith('sc1_') and scadenza < FRA_4_MESI:
                                prodotti_in_scadenza_all1.append((scadenza, prodotto))
                                setattr(verifica, 'ck_%s' % prodotto, 'table-warning')
                                verifica.save()
                        except TypeError:
                            pass

                    case '2':
                        try:
                            if prodotto.startswith('sc2_') and scadenza < FRA_4_MESI:
                                prodotti_in_scadenza_all2.append((scadenza, prodotto))
                                setattr(verifica, 'ck_%s' % prodotto, 'table-warning')
                                verifica.save()
                        except TypeError:
                            pass

        prodotti_in_scadenza_all1.sort()
        prodotti_in_scadenza_all2.sort()

        scadenze_all1 = {}
        scadenze_all2 = {}
        for data, prodotto in prodotti_in_scadenza_all1:
            try:
                scadenze_all1[(data, prodotto[4:])] += 1

            except KeyError:
                scadenze_all1[(data, prodotto[4:])] = 1

        for data, prodotto in prodotti_in_scadenza_all2:
            try:
                scadenze_all2[(data, prodotto[4:])] += 1

            except KeyError:
                scadenze_all2[(data, prodotto[4:])] = 1

        prodotti_all1 = [(x[0].strftime('%m/%Y'), x[1], scadenze_all1[x]) for x in scadenze_all1]
        prodotti_all2 = [(x[0].strftime('%m/%Y'), x[1], scadenze_all2[x]) for x in scadenze_all2]
        return prodotti_all1, prodotti_all2

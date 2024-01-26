import datetime
import inspect
from pprint import pprint as pp

OGGI = datetime.date.today()
FRA_4_MESI = OGGI + datetime.timedelta(days=30.5 * 6)


class Cassetta_PS_Util:
    def __init__(self, verifica):
        self.verifiche = verifica


    def prodotti_in_scadenza(self):
        prodotti_in_scadenza = []
        for verifica in self.verifiche:

            for prodotto, scadenza in inspect.getmembers(verifica):

                try:
                    if prodotto.startswith('sc2_') and scadenza < FRA_4_MESI:
                        prodotti_in_scadenza.append((scadenza, prodotto))

                except TypeError:
                    pass

        prodotti_in_scadenza.sort()
        pp(prodotti_in_scadenza)
        print()

        scadenze = {}
        for data, prodotto in prodotti_in_scadenza:
            try:
                scadenze[(data, prodotto[4:])] += 1

            except KeyError:
                scadenze[(data, prodotto[4:])] = 1

        for x in scadenze:
            print(x, scadenze[x])

        prodotti = [(x[0].strftime('%m/%Y'), x[1], scadenze[x]) for x in scadenze]
        return prodotti
import datetime
import inspect

OGGI = datetime.date.today()
FRA_4_MESI = OGGI + datetime.timedelta(days=30.5 * 24)


class Cassetta:
    def __init__(self, verifica):
        self.verifica = verifica

    def prodotti_in_scadenza(self):
        scadenze_prodotti = []
        for prodotto, scadenza in inspect.getmembers(self.verifica):

            try:
                if prodotto.startswith('sc2_') and scadenza < FRA_4_MESI:
                    scadenze_prodotti.append((scadenza, prodotto))
            except TypeError:
                pass

            # try:
            #     if prodotto.startswith('sc2_') and scadenza < FRA_4_MESI:
            #         # print(prodotto, scadenza)
            #         try:
            #             scadenze_prodotti[scadenza].append(prodotto)
            #         except KeyError:
            #             scadenze_prodotti[scadenza] = [prodotto, ]
            #
            # except TypeError:
            #     pass

        return scadenze_prodotti

import datetime
import inspect
from icecream import ic
from .models import VerificaCassettaPS

# from pprint import pprint as pp

OGGI = datetime.date.today()
FRA_4_MESI = OGGI + datetime.timedelta(days=30.5 * 6)

PRODOTTI_ALL1 = {
    'guanti': "Guanti sterili monouso (x5)",
    'iodio': "Flacone soluzione cutanea di iodopovidone (10% iodio) 1 litro",
    'fisiologica': "Flacone soluzione fisiologica (sodio cloruro 0,9%) 500ml (x3)",
    'garza10x10': "Compresse di garza sterile 10x10 in buste singole (x10)",
    'garza18x40': "Compresse di garza sterile 18x40 in buste singole (x2)",
    'pinzette': "Pinzette di medicazione monouso (x2)",
    'cotone': "Confezione di cotone idrofilo",
    'cerotti': "Confezioni di cerotti di varie misure pronte all'uso (x2)",
    'cerotto25': "Rotoli di cerotto alto 2.5cm (x2)",
    'visiera': "Visiera paraschizzi",
    'forbici': "Un paio di forbici",
    'laccio': "Lacci emostatici (x3)",
    'ghiaccio': "Ghiaccio pronto all'uso (x2)",
    'sacchetto': "Sacchetti monouso per la raccolta di rifiuti sanitari (x2)",
    'teli': "Teli sterili monouso (2)",
    'rete': "Confezione di rete elastica di misura media (x2)",
    'termometro': "Termometro",
    'sfigmomanometro': "Apparecchio per la misurazione della pressione arteriosa",
    'istruzioni': "Istruzioni sul modo di usare i presidi e prestare i primi soccorsi",
}

PRODOTTI_ALL2 = {
    'guanti': 'Guanti sterili monouso (x2)',
    'iodio': 'Flacone soluzione cutanea di iodopovidone (10% iodio) 125ml',
    'fisiologica': 'Flacone soluzione fisiologica (Sodio cloruro 0,9%) da 250ml',
    'garza18x40': 'Compressa garza sterile 18x40 in buste singole',
    'garza10x10': 'Compressa garza sterile 10x10 in buste singole (x3)',
    'pinzette': 'Pinzette di medicazione monouso',
    'cotone': 'Confezione di cotone idrofilo',
    'cerotti': "Confezioni di cerotti di varie misure pronte all'uso",
    'cerotto25': 'Rotoli di cerotto alto 2.5cm',
    'benda10': 'Rotolo di benda orlata alta 10cm',
    'forbici': 'Un paio di forbici',
    'laccio': 'Laccio emostatico',
    'ghiaccio': "Ghiaccio pronto all'uso",
    'sacchetti': 'Sacchetti monouso per la raccolta di rifiuti sanitari',
    'istruzioni': 'Istruzioni ed estratto D.Lgs 81/08',
}


class Cassetta_PS_Util:
    # todo: obsoleto
    def __init__(self, verifica):
        self.verifiche = verifica

    def prodotti_in_scadenza(self):
        prodotti_in_scadenza_all1 = []
        prodotti_in_scadenza_all2 = []
        for verifica in self.verifiche:

            for prodotto, scadenza in inspect.getmembers(verifica):
                # ic(scadenza)

                match verifica.cassetta.allegato:
                    case '1':
                        try:
                            if prodotto.startswith('sc1_'):
                                setattr(verifica, 'ck_%s' % prodotto, '')

                                if scadenza < OGGI:
                                    prodotti_in_scadenza_all1.append((scadenza, prodotto))
                                    setattr(verifica, 'ck_%s' % prodotto, 'table-danger')

                                elif scadenza < FRA_4_MESI:
                                    prodotti_in_scadenza_all1.append((scadenza, prodotto))
                                    setattr(verifica, 'ck_%s' % prodotto, 'table-warning')

                                verifica.save()

                        except TypeError:
                            pass

                    case '2':
                        try:
                            if prodotto.startswith('sc2_'):
                                setattr(verifica, 'ck_%s' % prodotto, '')

                                if scadenza < OGGI:
                                    prodotti_in_scadenza_all2.append((scadenza, prodotto))
                                    setattr(verifica, 'ck_%s' % prodotto, 'table-danger')

                                elif scadenza < FRA_4_MESI:
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

        prodotti_all1 = [(x[0].strftime('%m/%y'), PRODOTTI_ALL1[x[1]], scadenze_all1[x]) for x in scadenze_all1]
        prodotti_all2 = [(x[0].strftime('%m/%y'), PRODOTTI_ALL2[x[1]], scadenze_all2[x]) for x in scadenze_all2]
        return prodotti_all1, prodotti_all2


class Cassetta_PS_Util2:
    def __init__(self, verifica):
        self.verifiche = verifica

    def _aggiorna_ck_sc_fields(self, instance, allegato='2'):
        prodotti_in_scadenza = []
        for field in instance._meta.fields:
            nome_field = field.name
            if nome_field.startswith(f'sc{allegato}_'):
                # Trova il nome del campo corrispondente 'ck_sc1_*'
                ck_field_name = f'ck_{nome_field}'

                # Controlla se esiste il campo ck_*
                if hasattr(instance, ck_field_name):
                    valore = getattr(instance, nome_field)

                    # ic(nome_field, valore)

                    try:
                        if valore < OGGI:
                            nuovo_valore = 'table-danger'
                            prodotti_in_scadenza.append((valore, nome_field))
                        elif valore < FRA_4_MESI:
                            nuovo_valore = 'table-warning'
                            prodotti_in_scadenza.append((valore, nome_field))
                        else:
                            nuovo_valore = ''

                        setattr(instance, ck_field_name, nuovo_valore)

                    except TypeError:
                        pass

        return prodotti_in_scadenza

    def aggiorna_stato_scadenza(self):
        verifiche = self.verifiche
        verifiche_all1 = [v for v in verifiche if v.cassetta.allegato == '1']
        verifiche_all2 = [v for v in verifiche if v.cassetta.allegato == '2']
        # ic(verifiche_all1)

        prodotti_in_scadenza_all1 = []
        for v in verifiche_all1:
            prodotti = self._aggiorna_ck_sc_fields(v, allegato=v.cassetta.allegato)
            prodotti_in_scadenza_all1.extend(prodotti)

        prodotti_in_scadenza_all2 = []
        for v in verifiche_all2:
            prodotti = self._aggiorna_ck_sc_fields(v, allegato=v.cassetta.allegato)
            prodotti_in_scadenza_all2.extend(prodotti)

        # # Salvi in bulk
        # VerificaCassettaPS.objects.bulk_update(verifiche, [f'ck_sc1_{name}' for name in [
        #     'guanti', 'iodio', 'fisiologica', 'garza10x10', 'garza18x40', 'pinzette',
        #     'cotone', 'cerotti', 'cerotto25', 'visiera', 'forbici', 'laccio', 'ghiaccio',
        #     'sacchetto', 'teli', 'rete', 'termometro', 'sfigmomanometro', 'istruzioni'
        # ]])

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

        prodotti_all1 = [(x[0].strftime('%m/%y'), PRODOTTI_ALL1[x[1]], scadenze_all1[x]) for x in scadenze_all1]
        prodotti_all2 = [(x[0].strftime('%m/%y'), PRODOTTI_ALL2[x[1]], scadenze_all2[x]) for x in scadenze_all2]

        return prodotti_all1, prodotti_all2

import configparser
from itertools import islice
import math
from pprint import pprint as pp

N_COLONNE = 6
CFG = 'estrai.cfg'


def chunk(arr_range, arr_size):
    arr_range = iter(arr_range)
    return iter(lambda: tuple(islice(arr_range, arr_size)), ())


def dividi_elenco_lavoratori(lavoratori, n_colonne=N_COLONNE):
    nlavoratori = len(lavoratori)
    gruppi = chunk(lavoratori, math.ceil(nlavoratori / n_colonne))
    return gruppi, n_colonne


class Estrai_Dati():
    def __int__(self):
        print('ciaoo ' * 20)

    def salva_lavoratori(self, lavoratori):
        config = configparser.ConfigParser()
        config.read(CFG)

        lavoratori = [lavoratore.id for lavoratore in lavoratori]
        config['DEFAULT'] = {'lavoratori': lavoratori}

        with open(CFG, 'w') as cfg:
            config.write(cfg)

    def estrai(self, elenco_lavoratori, elenco_formazione, elenco_nomine):
        tabella = []
        for lavoratore in elenco_lavoratori:
            cognome, nome = lavoratore.lavoratore.cognome, lavoratore.lavoratore.nome
            rigo = [(cognome, nome), ]

            # todo: campo *_ck non funzionante
            attestati = [(getattr(lavoratore, formazione), getattr(lavoratore, '{}_ck'.format(formazione))) for
                         formazione in elenco_formazione]
            rigo.append(attestati)

            nomine = [getattr(lavoratore, nomina) for nomina in elenco_nomine]
            rigo.append(nomine)

            tabella.append(rigo)

        # pp(tabella)

        return tabella

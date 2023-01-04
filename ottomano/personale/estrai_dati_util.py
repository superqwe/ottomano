import configparser
from itertools import islice

from pprint import pprint as pp

N_COLONNE = 6
CFG = 'estrai.cfg'


def chunk(arr_range, arr_size):
    arr_range = iter(arr_range)
    return iter(lambda: tuple(islice(arr_range, arr_size)), ())


def dividi_elenco_lavoratori(lavoratori):
    nlavoratori = len(lavoratori)
    gruppi = chunk(lavoratori, nlavoratori // N_COLONNE)

    return gruppi, N_COLONNE


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

import datetime
import os.path

DURATA_CORSI = {
    'art37': 5,
    'aspp': 5,
    'autogru': 5,
    'carrello': 5,
    'dirigente': 5,
    'ept': 5,
    'dumper': 5,
    'gru_autocarro': 5,
    'imbracatore': 5,
    'ple': 5,
    'ponteggiatore': 4,
    'primo_soccorso': 3,
    'rls': 1,
    'rullo': 5,
    'sollevatore': 5,
    'spazi_confinati': 5,
}


def calcola_data_scadenza(data_corso, durata):
    data_corso = datetime.datetime.strptime(data_corso, '%d%m%y')
    data_scadenza = datetime.date(data_corso.year + durata, data_corso.month, data_corso.day)

    return data_scadenza, data_corso


def calcola_data_scadenza_preposto(data_corso):
    data_corso = datetime.datetime.strptime(data_corso, '%d%m%y')

    if data_corso >= datetime.datetime(2022, 6, 1):
        data_scadenza = datetime.date(data_corso.year + 2, data_corso.month, data_corso.day)
    else:
        data_scadenza = datetime.date(data_corso.year + 5, data_corso.month, data_corso.day)

    return data_scadenza, data_corso


def calcola_data_attestati(attestati, lavoratore):
    attestati_ = []
    for attestato in attestati:
        corso, data_dc = os.path.splitext(attestato)[0].split()

        match corso:
            case 'antincendio':
                # todo: da sistemare
                data_scadenza, data_corso = calcola_data_scadenza(data_dc, 5)
            case 'preposto':
                data_scadenza, data_corso = calcola_data_scadenza_preposto(data_dc)
            case 'amianto' | 'dpi3' | 'formatore' | 'lavori_quota' | 'mmt' | 'rir' | 'spazi_confinati_lc':
                print('*** attestato non riconosciuto ***', lavoratore, attestato)
                continue
            case _:
                durata = DURATA_CORSI[corso]
                data_scadenza, data_corso = calcola_data_scadenza(data_dc, durata)

        attestati_.append((corso, data_corso, data_scadenza))

    return attestati_

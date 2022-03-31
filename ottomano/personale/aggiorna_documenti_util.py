import datetime
import os.path

DURATA_CORSI = {
    'art37': 5,
    'aspp': 5,
    'autogru': 5,
    'carrello': 5,
    'dirigente': 5,
    'ept': 5,
    'gru_autocarro': 5,
    'imbracatore': 5,
    'ple': 5,
    'ponteggiatore': 4,
    'primo_soccorso': 3,
    'rls': 1,
    'sollevatore': 5,
    'spazi_confinati': 5,
}


def calcola_data_scadenza(data_corso, durata):
    data = datetime.datetime.strptime(data_corso, '%d%m%y')
    data = datetime.date(data.year + durata, data.month, data.day)

    return data


def calcola_data_attestati(attestati, lavoratore):
    attestati_ = []
    for attestato in attestati:
        corso, data = os.path.splitext(attestato)[0].split()

        match corso:
            case 'antincendio':
                # todo: da sistemare
                data = calcola_data_scadenza(data, 5)
            case 'preposto':
                # todo: da sistemare
                data = calcola_data_scadenza(data, 5)
            case 'amianto' | 'dpi3' | 'formatore' | 'spazi_confinati_lc':
                print('*** attestato non riconosciuto ***', lavoratore, attestato)
                continue
            case _:
                durata = DURATA_CORSI[corso]
                data = calcola_data_scadenza(data, durata)

        attestati_.append((corso, data))

    return attestati_

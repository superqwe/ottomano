import csv
import pathlib
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render
from personale.models import Lavoratore
from sgi.models import Formazione, Non_Conformita, DPI2

PATH_DOCUMENTI = pathlib.Path(r'C:\Users\L. MASI\Documents\Documenti_Lavoratori')
FORMAZIONE_ANNO = 2023
FORMAZIONE_FRAZIONI_ORE = {
    '10min': 1 / 6,
    '15min': 0.25,
    '30min': 0.5,
    '1.5': 1.5,
    '1,5': 1.5,
}


def index(request):
    """"importa csv"""
    MESE = {'Gennaio': '01',
            'Febbraio': '02',
            'Marzo': '03',
            'Aprile': '04',
            'Maggio': '05',
            'Giugno': '06',
            'Luglio': '07',
            'Agosto': '08',
            'Settembre': '09',
            'Ottobre': '10',
            'Novembre': '11',
            'Dicembre': '12',
            }
    with open(r'C:\Users\benedetto.basile\Dropbox\SGI\Formazione\importare.csv') as file:
        reader = csv.reader(file, dialect='excel', delimiter=';')
        next(reader)  # Advance past the header

        for row in reader:
            mese, corso, data, argomento, docente, ore, persone = row[:-1]

            mese = MESE[mese]
            data = datetime.strptime(data, '%d/%m/%Y').date()
            corso = corso if corso else None

            print(mese, corso, data, argomento, docente, ore, persone)

            formazione = Formazione(mese=mese, corso=corso, data=data, argomento=argomento, docente=docente, ore=ore,
                                    persone=persone
                                    )
            # formazione.save()

    return HttpResponse("Hello, world. You're at the personale index.")


def formazione(request, anno=FORMAZIONE_ANNO):
    formazione_ = Formazione.objects.filter(data__year=anno)

    # sessioni
    corsi_totali = formazione_.count()
    corsi_esterni = formazione_.filter(corso=None).count()
    corsi_interni = corsi_totali - corsi_esterni

    # ore
    ore_interno = ore_esterno = 0
    for corso in formazione_:
        if corso.ore.isnumeric():
            ore = int(corso.ore) * int(corso.persone)
        else:
            ore = FORMAZIONE_FRAZIONI_ORE[corso.ore] * int(corso.persone)

        if corso.corso:
            ore_interno += ore
        else:
            ore_esterno += ore

    ore_totali = ore_interno + ore_esterno

    # ore media persona
    n_lavoratori = Lavoratore.objects.filter(in_forza=True).count()
    media_interna = ore_interno / n_lavoratori
    media_esterna = ore_esterno / n_lavoratori
    media_totale = ore_totali / n_lavoratori

    # statistiche ore
    statistiche = (
        ('Corsi interni', corsi_interni, ore_interno, media_interna),
        ('Corsi esterni', corsi_esterni, ore_esterno, media_esterna),
        ('Totale', corsi_totali, ore_totali, media_totale)
    )

    context = {'titolo': 'Programma di informazione, formazione, addestramento',
               'pagina_attiva_formazione': 'active',
               'sezione_sgi_attiva': 'active',
               'formazione': formazione_,
               'statistiche': statistiche
               }

    pagina_attiva_formazione_2023 = pagina_attiva_formazione_2022 = ''

    match anno:
        case 2023:
            pagina_attiva_formazione_2023 = 'active'
        case 2022:
            pagina_attiva_formazione_2022 = 'active'

    context['pagina_attiva_formazione_2023'] = pagina_attiva_formazione_2023
    context['pagina_attiva_formazione_2022'] = pagina_attiva_formazione_2022

    return render(request, 'sgi/formazione.html', context)


def non_conformita(request, anno=FORMAZIONE_ANNO):
    non_conformita_ = Non_Conformita.objects.filter(data__year=anno).order_by('-data')

    context = {'titolo': 'Registro Non Conformità',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_nc': 'active',
               'elenco_non_conformita': non_conformita_,
               }

    pagina_attiva_formazione_2023 = pagina_attiva_formazione_2022 = ''

    match anno:
        case 2023:
            pagina_attiva_formazione_2023 = 'active'
        case 2022:
            pagina_attiva_formazione_2022 = 'active'

    context['pagina_attiva_formazione_2023'] = pagina_attiva_formazione_2023
    context['pagina_attiva_formazione_2022'] = pagina_attiva_formazione_2022

    return render(request, 'sgi/non_conformita.html', context)


def scadenzario_dpi(request):
    lavoratori = Lavoratore.objects.filter(in_forza=True)

    for lavoratore in lavoratori:
        cognome, nome = lavoratore.cognome, lavoratore.nome
        path_lavoratore = PATH_DOCUMENTI.joinpath('{} {}'.format(cognome, nome))
        consegna_dpi = list(path_lavoratore.glob('consegna_dpi*'))

        try:
            dpi = DPI2.objects.get(lavoratore__cognome__iexact=cognome, lavoratore__nome__iexact=nome)
        except ObjectDoesNotExist:
            lavoratore = Lavoratore.objects.get(cognome__iexact=cognome, nome__iexact=nome)
            dpi = DPI2(lavoratore=lavoratore)

        if consegna_dpi:
            data_consegna = consegna_dpi[0].name.split()[1].split('.')[0]
            data_consegna = datetime.strptime(data_consegna, '%d%m%y')
            dpi.consegna = data_consegna

        dpi.save()

    # aggiorna data scadenza elemetto
    lista_dpi = DPI2.objects.filter(lavoratore__in_forza=True).exclude(lavoratore__cantiere__cantiere='Uffici Sede')

    for dpi in lista_dpi:
        data_fabbrica = dpi.elmetto_df

        if data_fabbrica:
            dpi.elmetto = datetime(data_fabbrica.year + 5, data_fabbrica.month, data_fabbrica.day)
            dpi.save()

    context = {'titolo': 'Scadenzario DPI',
               'sezione_sgi_attiva': 'active',
               'pagina_attiva_scadenzario_dpi': 'active',
               }

    return render(request, 'sgi/scadenzario_dpi.html', context)

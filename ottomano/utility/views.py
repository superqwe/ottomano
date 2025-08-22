from django.shortcuts import render
from personale.models import Lavoratore, Formazione, Idoneita, DPI
from utility import estrai_dati_util


# Create your views here.

def estrai_dati(request):
    lavoratori = Formazione.objects.filter(lavoratore__in_forza=True).exclude(
        lavoratore__cantiere__cantiere='Uffici Sede').exclude(
        lavoratore__cognome='Ottomano'
    )

    gruppi_lavoratori, n_gruppi_lavoratori = estrai_dati_util.dividi_elenco_lavoratori(lavoratori)

    formazione = (
        'preposto', 'primo_soccorso', 'antincendio', 'art37', 'spazi_confinati', 'ponteggiatore', 'imbracatore', 'mmc',
        'ept', 'dumper', 'rullo', 'autogru', 'gru_autocarro', 'carrello', 'sollevatore', 'ple', 'rls', 'aspp')

    gruppi_formazione, n_gruppi_formazione = estrai_dati_util.dividi_elenco_lavoratori(formazione, 3)

    nomine = ['nomina_{}'.format(x) for x in
              ('preposto', 'preposto_imbracatore', 'antincendio', 'primo_soccorso', 'aspp')]

    context = {'titolo': 'Estrai Dati',
               'sezione_utility_attiva': 'active',
               'pagina_attiva_estrai_dati': 'active',
               'n_gruppi_lavoratori': n_gruppi_lavoratori,
               'gruppi_lavoratori': gruppi_lavoratori,
               'n_gruppi_formazione': n_gruppi_formazione,
               'gruppi_formazione': gruppi_formazione,
               'nomine': nomine,
               }

    return render(request, 'utility/estrai_dati.html', context)


def dati_estratti(request):
    if request.method == 'POST':

        lavoratori = []
        attestati = []
        nomine = []
        documenti_vari = []
        for x in request.POST.keys():
            # ic(x)
            if x != 'csrfmiddlewaretoken':
                if x.isnumeric():
                    lavoratore = Formazione.objects.get(id__exact=x)
                    lavoratori.append(lavoratore)
                elif x.startswith('nomina_'):
                    nomine.append(x)
                elif x.startswith(('unilav', 'idoneita', 'consegna_dpi')):
                    documenti_vari.append(x)
                else:
                    attestati.append(x)

        dati = estrai_dati_util.Estrai_Dati()

        tabella, zip_file_nome, file_non_trovati = dati.estrai(lavoratori, attestati, nomine, documenti_vari)

        documenti_vari = ['Idoneità' if x == 'idoneita' else x for x in documenti_vari]

        documenti = attestati
        documenti.extend(nomine)
        documenti.extend(documenti_vari)

        context = {'titolo': 'Dati Estratti',
                   'sezione_utility_attiva': 'active',
                   'pagina_attiva_estrai_dati': 'active',
                   'lavoratori': lavoratori,
                   'documenti': documenti,
                   'tabella': tabella,
                   'zip': zip_file_nome,
                   'file_non_trovati': file_non_trovati
                   }

        return render(request, 'utility/dati_estratti.html', context)

    return


def documenti_controlla(request):
    context = {'titolo': 'Controlla Documenti',
               'sezione_utility_attiva': 'active',
               'pagina_attiva_controlla_documenti': 'active',
               }
    
    return render(request, 'utility/controlla_documenti_attendi.html', context)


def documenti_controllati(request):
    context = {'titolo': 'Controlla Documenti',
               'sezione_utility_attiva': 'active',
               'pagina_attiva_controlla_documenti': 'active',
               }

    return render(request, 'utility/controlla_documenti_controllati.html', context)

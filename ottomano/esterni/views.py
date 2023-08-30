from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from personale.models import Lavoratore, Formazione, Idoneita
from .models import Cantiere_Esterno


def index(request):
    cantieri = Cantiere_Esterno.objects.filter(in_corso=True)
    context = {'titolo': 'Cantieri Esterni',
               'pagina_attiva_esterni': 'active',
               'sezione_esterni_attiva': 'active',
               'cantieri': cantieri,
               # 'conteggio_rg': conteggio_rg(formazione_)
               }
    return render(request, 'esterni/elenco cantieri.html', context)


def lavoratori(request, id_cantiere):
    cantiere = Cantiere_Esterno.objects.get(id=id_cantiere)
    elenco_lavoratori = cantiere.elenco_lavoratori.all()

    context = {'titolo': cantiere,
               'id_cantiere': id_cantiere,
               'pagina_attiva_esterni_lavoratori': 'active',
               'sezione_esterni_attiva': 'active',
               'elenco_lavoratori': elenco_lavoratori,
               }
    return render(request, 'esterni/lavoratori.html', context)


def mezzi(request, id_cantiere):
    cantiere = Cantiere_Esterno.objects.get(id=id_cantiere)
    elenco_mezzi = cantiere.elenco_mezzi.all()

    context = {'titolo': cantiere,
               'id_cantiere': id_cantiere,
               'pagina_attiva_esterni_mezzi': 'active',
               'sezione_esterni_attiva': 'active',
               'mezzi': elenco_mezzi,
               }
    return render(request, 'esterni/mezzi.html', context)


def documentazione(request, id_cantiere):
    cantiere = Cantiere_Esterno.objects.get(id=id_cantiere)
    elenco_mezzi = cantiere.elenco_mezzi.all()

    context = {'titolo': cantiere,
               'id_cantiere': id_cantiere,
               'pagina_attiva_esterni_documentazione': 'active',
               'sezione_esterni_attiva': 'active',
               'mezzi': elenco_mezzi,
               }
    return render(request, 'esterni/documentazione_cantieri/%s.html' % cantiere, context)

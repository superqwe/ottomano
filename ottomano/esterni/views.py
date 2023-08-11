from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from personale.models import Lavoratore, Formazione, Idoneita
from .models import Cantiere_Esterno


def index(request):
    cantieri = Cantiere_Esterno.objects.filter(in_corso=True)
    context = {'titolo': 'Cantieri Estreni',
               'pagina_attiva_esterni': 'active',
               'sezione_esterni_attiva': 'active',
               'cantieri': cantieri,
               # 'conteggio_rg': conteggio_rg(formazione_)
               }
    return render(request, 'esterni/elenco cantieri.html', context)


def lavoratori(request, id_cantiere):
    cantiere = Cantiere_Esterno.objects.get(id=id_cantiere)
    elenco_lavoratori = cantiere.elenco_lavoratori.all()
    print(elenco_lavoratori)
    # for x in elenco_lavoratori:
    #     print(x.nome)

    context = {'titolo': cantiere,
               'id_cantiere': id_cantiere,
               'pagina_attiva_esterni_lavoratori': 'active',
               'sezione_esterni_attiva': 'active',
               # 'elenco_lavoratori': elenco_lavoratori,
               # 'conteggio_rg': conteggio_rg(formazione_)
               }
    return render(request, 'esterni/lavoratori.html', context)


def mezzi(request, id_cantiere):
    return HttpResponse("Hello, world. You're at the esterni index.")


def documentazione(request, id_cantiere):
    return HttpResponse("Hello, world. You're at the esterni index.")

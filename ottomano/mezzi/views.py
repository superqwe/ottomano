from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render
# import personale.importa_dati
from django.core.exceptions import ObjectDoesNotExist
from mezzi.models import Mezzo

from pprint import pprint as pp


def index(request):
    return HttpResponse("Hello, world. You're at the mezzi index.")


def elenco(request):
    mezzi = Mezzo.objects.filter(in_forza=True)
    context = {'titolo': 'Elenco Mezzi',
               'pagina_attiva_elenco': 'active',
               'mezzi': mezzi}

    return render(request, 'mezzi/base.html', context)


def scadenziario(request):
    return HttpResponse("Hello, world. You're at the mezzi index.")


def aggiorna_documenti(request):
    return HttpResponse("Hello, world. You're at the mezzi index.")


def aggiorna_stato(request):
    return HttpResponse("Hello, world. You're at the mezzi index.")

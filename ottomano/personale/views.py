from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

import personale.importa_dati


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def importa_Personale_abilitazioni(request):
    personale.importa_dati.importa_xlsx()
    return HttpResponse("xls importato")

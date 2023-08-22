
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


from pprint import pprint as pp


def index(request):
    return HttpResponseRedirect("/personale/formazione")

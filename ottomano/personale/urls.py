from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('importa_Personale_abilitazioni', views.importa_Personale_abilitazioni, name='importa_Personale_abilitazioni'),
    path('anagrafica', views.anagrafica, name='anagrafica'),
]
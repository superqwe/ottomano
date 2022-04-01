from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('importa_Personale_abilitazioni', views.importa_Personale_abilitazioni, name='importa_Personale_abilitazioni'),
    path('anagrafica', views.anagrafica, name='anagrafica'),
    path('aggiorna_documenti', views.aggiorna_documenti, name='aggiorna_documenti'),
    path('aggiorna_stato', views.aggiorna_stato, name='aggiorna_stato'),
    path('formazione', views.formazione, name='formazione'),
    path('idoneita', views.idoneita, name='idoneita'),
    path('scadenziario_formazione', views.scadenziario_formazione, name='scadenziario_formazione'),
    path('scadenziario_idoneita', views.scadenziario_idoneita, name='scadenziario_idoneita'),
]
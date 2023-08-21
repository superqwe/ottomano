from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('anagrafica', views.anagrafica, name='anagrafica'),
    path('aggiorna_documenti', views.aggiorna_documenti, name='aggiorna_documenti'),
    path('aggiorna_stato', views.aggiorna_stato, name='aggiorna_stato'),
    path('estrai_dati', views.estrai_dati, name='estrai_dati'),
    path('dati_estratti', views.dati_estratti, name='dati_estratti'),
    path('formazione', views.formazione, name='formazione'),
    path('idoneita', views.idoneita, name='idoneita'),
    path('scadenzario_dpi', views.scadenzario_dpi, name='scadenzario_dpi'),
    path('scadenziario_formazione', views.scadenziario_formazione, name='scadenziario_formazione'),
    path('scadenziario_idoneita', views.scadenziario_idoneita, name='scadenziario_idoneita'),
]
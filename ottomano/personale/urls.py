from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('anagrafica', views.anagrafica, name='anagrafica'),
    path('aggiorna_documenti', views.aggiorna_documenti2, name='aggiorna_documenti2'),
    path('aggiorna_stato', views.aggiorna_stato4, name='aggiorna_stato4'),
    # path('estrai_dati', views.estrai_dati, name='estrai_dati'),
    # path('dati_estratti', views.dati_estratti, name='dati_estratti'),
    path('formazione', views.formazione, name='formazione'),
    path('scadenzario_formazione', views.scadenziario_formazione, name='scadenzario_formazione'),
    path('scadenzario_formazione_schede/<slug:anno>/', views.scadenzario_formazione_schede,
         name='scadenzario_formazione_schede'),
    path('idoneita', views.idoneita, name='idoneita'),
    path('scadenzario_idoneita', views.scadenzario_idoneita, name='scadenzario_idoneita'),
]

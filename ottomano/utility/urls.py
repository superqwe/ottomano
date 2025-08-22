from django.urls import path

from . import views

urlpatterns = [
    path('estrai_dati', views.estrai_dati, name='estrai_dati'),
    path('dati_estratti', views.dati_estratti, name='dati_estratti'),
    path('documenti_controlla', views.documenti_controlla, name='documenti_controlla'),
    path('documenti_controllati', views.documenti_controllati, name='documenti_controllati'),
]

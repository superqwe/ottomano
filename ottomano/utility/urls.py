from django.urls import path

from . import views

app_name = 'utility'

urlpatterns = [
    path('estrai_dati/', views.estrai_dati, name='estrai_dati'),
    path('dati_estratti/', views.dati_estratti, name='dati_estratti'),
    path('documenti_controllati/', views.documenti_controllati2, name='documenti_controllati'),
    path('log/<str:livello>/', views.log, name='log'),
]

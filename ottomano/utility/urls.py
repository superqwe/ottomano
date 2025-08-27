from django.urls import path

from . import views

app_name = 'utility'

urlpatterns = [
    path('estrai_dati/', views.estrai_dati, name='estrai_dati'),
    path('dati_estratti/', views.dati_estratti, name='dati_estratti'),
    path('documenti_controllati/', views.documenti_controllati2, name='documenti_controllati'),
    path('log/<str:livello>/', views.log, name='log'),
    path('db_bck/', views.db_bck, name='db_bck'),
    path('db_bck/crea/', views.db_bck_crea, name='db_bck_crea'),
]

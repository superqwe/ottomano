from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aggiorna_documenti', views.aggiorna_documenti, name='aggiorna_documenti'),
    path('elenco', views.elenco, name='elenco'),
]

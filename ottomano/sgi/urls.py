from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('formazione/', views.formazione, name='formazione'),
    path('formazione/<int:anno>/', views.formazione, name='formazione'),
    path('non_conformita/', views.non_conformita, name='non_conformita'),
    path('non_conformita/<int:anno>/', views.non_conformita, name='non_conformita'),
    path('near_miss/', views.near_miss, name='near_miss'),
    path('near_miss/<int:anno>/', views.near_miss, name='near_miss'),
    path('scadenzario_dpi/', views.scadenzario_dpi, name='scadenzario_dpi'),
    path('scadenzario_dpi_aggiorna/', views.scadenzario_dpi_aggiorna, name='scadenzario_dpi_aggiorna'),
    path('cassette_ps/', views.cassette_ps, name='cassette_ps'),
    path('cassette_ps_storico/', views.cassette_ps_storico, name='cassette_ps_storico'),
    path('cassette_ps_storico/<int:anno>/', views.cassette_ps_storico, name='cassette_ps_storico'),
    path('cassette_ps_scadenze/', views.cassette_ps_scadenze, name='cassette_ps_contenuto'),
    path('rilevatorih2s/', views.rilevatorih2s, name='rilevatorih2s'),
    path('accessori_sollevamento/', views.accessori_sollevamento, name='accessori_sollevamento'),
    path('dpi_anticaduta/', views.dpi_anticaduta_registro, name='dpi_anticaduta'),
    path('dpi_anticaduta/registro', views.dpi_anticaduta_registro, name='dpi_anticaduta_registro'),
    path('dpi_anticaduta/elenco', views.dpi_anticaduta_elenco, name='dpi_anticaduta_elenco'),
    path('dpi_anticaduta/storia', views.dpi_anticaduta_storia, name='dpi_anticaduta_storia'),
    path('formazione_cantieri/', views.formazione_cantieri, name='formazione_cantieri'),
]

# urlpatterns = [
#     # ... the rest of your URLconf goes here ...
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

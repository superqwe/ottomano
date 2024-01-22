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
    path('scadenzario_dpi/', views.scadenzario_dpi, name='scadenzario_dpi'),
    path('scadenzario_dpi_aggiorna/', views.scadenzario_dpi_aggiorna, name='scadenzario_dpi_aggiorna'),
    path('cassette_ps/', views.cassette_ps, name='cassette_ps'),
    path('cassette_ps_storico/', views.cassette_ps_storico, name='cassette_ps_storico'),
    path('cassette_ps_scadenze/', views.cassette_ps_scadenze, name='cassette_ps_contenuto'),
    path('rilevatorih2s/', views.rilevatorih2s, name='rilevatorih2s'),
]

# urlpatterns = [
#     # ... the rest of your URLconf goes here ...
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

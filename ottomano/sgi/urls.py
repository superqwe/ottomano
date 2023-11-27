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
]

# urlpatterns = [
#     # ... the rest of your URLconf goes here ...
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

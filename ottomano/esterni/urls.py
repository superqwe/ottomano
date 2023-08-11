from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lavoratori', views.lavoratori, name='lavoratori'),
    path('lavoratori/<int:id_cantiere>', views.lavoratori, name='lavoratori'),
    path('mezzi/<int:id_cantiere>', views.mezzi, name='mezzi'),
    path('documentazione/<int:id_cantiere>', views.documentazione, name='documentazione'),
]

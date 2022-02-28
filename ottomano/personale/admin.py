from django.contrib import admin

from .models import Lavoratore, Formazione


# Register your models here.

class LavoratoreAdmin(admin.ModelAdmin):
    list_display = (
        'in_forza', 'cognome', 'nome', 'cellulare', 'data_fine', 'qualifica', 'assunzione', 'mansione',
        'attivita_svolta', 'mansione_1', 'mansione_2', 'mansione_3', 'reparto')
    list_display_links = ('cognome', 'nome')
    list_filter = ('in_forza', 'reparto')


class FormazioneAdmin(admin.ModelAdmin):
    list_display = ('lavoratore', 'art37', 'preposto', 'primo_soccorso', 'antincendio')
    # list_display_links = ('cognome', 'nome')
    # list_filter =('in_forza', 'reparto')


admin.site.register(Lavoratore, LavoratoreAdmin)
admin.site.register(Formazione, FormazioneAdmin)

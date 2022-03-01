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
    fields = (
        'lavoratore',
        ('preposto', 'preposto_ck'),
        ('primo_soccorso', 'primo_soccorso_ck'),
        ('antincendio', 'antincendio_ck'),
        ('art37', 'art37_ck'),
        ('spazi_confinati', 'spazi_confinati_ck'),
        ('ponteggiatore', 'ponteggiatore_ck'),
        ('imbracatore', 'imbracatore_ck'),
        ('ept', 'ept_ck'),
        ('autogru', 'autogru_ck'),
        ('gru_autocarro', 'gru_autocarro_ck'),
        ('carrello', 'carrello_ck'),
        ('ple', 'ple_ck'),
        ('rls', 'rls_ck'),
    )
    list_display = ('lavoratore', 'art37', 'preposto', 'primo_soccorso', 'antincendio')
    save_on_top = True
    # list_display_links = ('cognome', 'nome')
    # list_filter =('in_forza', 'reparto')


admin.site.register(Lavoratore, LavoratoreAdmin)
admin.site.register(Formazione, FormazioneAdmin)

from django.contrib import admin

from .models import Lavoratore, Formazione, Cantiere, Idoneita


# Register your models here.

class LavoratoreAdmin(admin.ModelAdmin):
    list_display = (
        'in_forza', 'cognome', 'nome', 'cellulare', 'data_fine', 'qualifica', 'assunzione', 'mansione',
        'attivita_svolta', 'mansione_1', 'mansione_2', 'mansione_3', 'reparto')
    list_display_links = ('cognome', 'nome')
    list_filter = ('in_forza', 'reparto')
    save_on_top = True


class FormazioneAdmin(admin.ModelAdmin):
    fields = (
        'lavoratore',
        ('preposto', 'preposto_ck', 'nomina_preposto'),
        ('primo_soccorso', 'primo_soccorso_ck', 'nomina_primo_soccorso'),
        ('antincendio', 'antincendio_ck', 'nomina_antincendio'),
        ('art37', 'art37_ck'),
        ('spazi_confinati', 'spazi_confinati_ck'),
        ('ponteggiatore', 'ponteggiatore_ck'),
        ('imbracatore', 'imbracatore_ck'),
        ('ept', 'ept_ck'),
        ('autogru', 'autogru_ck'),
        ('gru_autocarro', 'gru_autocarro_ck'),
        ('carrello', 'carrello_ck'),
        ('sollevatore', 'sollevatore_ck'),
        ('ple', 'ple_ck'),
        ('rls', 'rls_ck'),
        ('aspp', 'aspp_ck', 'nomina_aspp'),
    )
    list_display = ('lavoratore', 'art37', 'preposto', 'primo_soccorso', 'antincendio')
    save_on_top = True
    # list_display_links = ('cognome', 'nome')
    # list_filter =('in_forza', 'reparto')


class CantiereAdmin(admin.ModelAdmin):
    save_on_top = True


class IdoneitaAdmin(admin.ModelAdmin):
    fields = (
        'lavoratore',
        ('idoneita', 'idoneita_ck'),
        'otoprotettori',
        'guanti',
        'posture',
        ('carichi_10', 'carichi_15'),
        'sollecitazioni_arto_superiore_sinistro',
        'spazi_confinati',
        'mansioni_gravose',
        'temperature',
    )
    list_display = ('lavoratore', 'idoneita')
    save_on_top = True


admin.site.register(Lavoratore, LavoratoreAdmin)
admin.site.register(Formazione, FormazioneAdmin)
admin.site.register(Cantiere, CantiereAdmin)
admin.site.register(Idoneita, IdoneitaAdmin)

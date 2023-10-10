from django.contrib import admin

from .models import Lavoratore, Formazione, Cantiere, Idoneita, DPI


# Register your models here.

class LavoratoreAdmin(admin.ModelAdmin):
    list_display = (
        'in_forza', 'cognome', 'nome', 'cellulare', 'data_fine', 'qualifica', 'assunzione', 'mansione',
        'attivita_svolta', 'mansione_1', 'mansione_2', 'mansione_3', 'cantiere')
    list_display_links = ('cognome', 'nome')
    list_filter = ('in_forza', 'cantiere')
    save_on_top = True


class FormazioneAdmin(admin.ModelAdmin):
    fields = (
        'lavoratore',
        'stato',
        ('dirigente', 'dirigente_dc', 'dirigente_ck'),
        ('preposto', 'preposto_dc', 'preposto_ck', 'nomina_preposto', 'nomina_preposto_subappalti'),
        ('primo_soccorso', 'primo_soccorso_dc', 'primo_soccorso_ck', 'nomina_primo_soccorso'),
        ('antincendio', 'antincendio_dc', 'antincendio_ck', 'nomina_antincendio'),
        ('art37', 'art37_dc', 'art37_ck'),
        ('spazi_confinati', 'spazi_confinati_dc', 'spazi_confinati_ck'),
        ('ponteggiatore', 'ponteggiatore_dc', 'ponteggiatore_ck'),
        ('imbracatore', 'imbracatore_dc', 'imbracatore_ck', 'nomina_preposto_imbracatore'),
        ('ept', 'ept_dc', 'ept_ck'),
        ('dumper', 'dumper_dc', 'dumper_ck'),
        ('rullo', 'rullo_dc', 'rullo_ck'),
        ('autogru', 'autogru_dc', 'autogru_ck'),
        ('gru_autocarro', 'gru_autocarro_dc', 'gru_autocarro_ck'),
        ('carrello', 'carrello_dc', 'carrello_ck'),
        ('sollevatore', 'sollevatore_dc', 'sollevatore_ck'),
        ('ple', 'ple_dc', 'ple_ck'),
        ('rls', 'rls_dc', 'rls_ck'),
        ('aspp', 'aspp_dc', 'aspp_ck', 'nomina_aspp'),
    )
    list_display = ('lavoratore', 'stato', 'art37', 'preposto', 'primo_soccorso', 'antincendio')
    save_on_top = True
    # list_display_links = ('cognome', 'nome')
    list_filter = ('stato', 'lavoratore__in_forza', 'lavoratore__cantiere')


class CantiereAdmin(admin.ModelAdmin):
    save_on_top = True


class IdoneitaAdmin(admin.ModelAdmin):
    fields = (
        'lavoratore',
        ('idoneita', 'idoneita_ck'),
        ('otoprotettori', 'rumore50'),
        'guanti',
        'posture',
        ('carichi_10', 'carichi_15'),
        'sollecitazioni_arto_superiore_sinistro',
        'spazi_confinati',
        'mansioni_gravose',
        'temperature',
        'scale',
        'calzature',
        'lenti',
        'semestrale'
    )
    list_display = ('lavoratore', 'idoneita')
    save_on_top = True


class DPIAdmin(admin.ModelAdmin):
    fields = (
        'lavoratore',
        'consegna',
        ('elmetto', 'elmetto_df'),
        'maschera'
    )
    list_display = ('lavoratore', 'consegna', 'elmetto', 'maschera')
    list_filter = ('lavoratore__in_forza',)
    save_on_top = True


admin.site.register(Lavoratore, LavoratoreAdmin)
admin.site.register(Formazione, FormazioneAdmin)
admin.site.register(Cantiere, CantiereAdmin)
admin.site.register(Idoneita, IdoneitaAdmin)
admin.site.register(DPI, DPIAdmin)

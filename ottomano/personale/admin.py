from django.contrib import admin

from .models import Lavoratore, Formazione, Cantiere, Idoneita, Idoneita_Revisione


@admin.register(Lavoratore)
class LavoratoreAdmin(admin.ModelAdmin):
    fields = (
        'in_forza',
        'cantiere',
        'matricola',
        ('cognome', 'nome'),
        'cf',
        'sesso',
        ('data_nascita', 'luogo_nascita', 'provincia_nascita'),
        ('indirizzo', 'cap', 'citta', 'provincia'),
        ('cellulare', 'email'),
        ('tipo_contratto', 'data_inizio', 'data_fine'),
        'livello',
        'qualifica',
        'assunzione',
        'busta_paga',
        ('scadenza_ap', 'consegnato_ap')
    )
    list_display = (
        'in_forza', 'matricola', 'cognome', 'nome', 'cantiere', 'cf', 'data_nascita',
        'luogo_nascita', 'provincia_nascita', 'qualifica', 'scadenza_ap', 'consegnato_ap'
    )
    list_display_links = ('cognome', 'nome')
    list_filter = ('in_forza', 'cantiere', 'consegnato_ap')
    save_on_top = True


@admin.register(Formazione)
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
        ('mmc', 'mmc_dc', 'mmc_ck'),
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
    list_filter = ('stato', 'lavoratore__in_forza', 'lavoratore__cantiere')


@admin.register(Cantiere)
class CantiereAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Idoneita)
class IdoneitaAdmin(admin.ModelAdmin):
    fields = (
        'lavoratore',
        ('idoneita', 'idoneita_ck'),
        ('otoprotettori', 'rumore50'),
        'guanti',
        'posture',
        ('carichi_10', 'carichi_15'),
        ('sollecitazioni_arto_superiore_sinistro', 'sollecitazioni_spalla_sinistra',
         'sollecitazioni_rachide', 'flessioni_rachide'),
        'martello_pneumatico',
        'spazi_confinati',
        'altezza',
        'mansioni_gravose',
        ('temperature', 'sbalzi_termici'),
        'scale',
        ('calzature_plantare', 'calzature_plantare_morbido', 'calzature_leggere'),
        'lenti',
        'semestrale',
        'dpi_respiratori'
    )
    list_display = ('lavoratore', 'idoneita')
    save_on_top = True


@admin.register(Idoneita_Revisione)
class IdoneitaRevisioneAdmin(admin.ModelAdmin):
    fields = ('data', 'revisione')
    list_display = ('data', 'revisione')
    save_on_top = True

# admin.site.register(Cantiere, CantiereAdmin)

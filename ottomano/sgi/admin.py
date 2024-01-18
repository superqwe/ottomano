from django.contrib import admin

from .models import Formazione, Non_Conformita, DPI2, CassettaPS, VerificaCassettaPS, RilevatoreH2S


class FormazioneAdmin(admin.ModelAdmin):
    list_display = ('mese', 'corso', 'data', 'argomento', 'docente', 'ore', 'persone')
    date_hierarchy = 'data'
    save_on_top = True


class Non_ConformitaAdmin(admin.ModelAdmin):
    list_display = (
        'data', 'emittente', 'area', 'tipologia', 'descrizione', 'trattamento', 'causa', 'azione_correttiva'
    )
    date_hierarchy = 'data'
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


class CassettaPSAdmin(admin.ModelAdmin):
    fields = (
        'numero',
        'stato',
        'allegato',
        'ubicazione',
        ('messa_in_servizio', 'dismissione'),
        ('scadenza', 'ultima_verifica'),
    )
    # list_display = ('stato', 'numero', 'allegato', 'ubicazione')
    list_display = ('numero', 'stato', 'allegato', 'ubicazione', 'ultima_verifica', 'scadenza')
    list_filter = ('stato',)
    save_on_top = True


class VerificaCassettaPSAdmin(admin.ModelAdmin):
    fields = (
        'cassetta',
        'data_verifica',
        'data_scadenza',
        'operazione',
        ('materiale_integrato',
         'materiale_da_integrare'),
        'note',
    )
    list_display = ('cassetta', 'data_verifica', 'data_scadenza', 'operazione', 'note', 'materiale_integrato',
                    'materiale_da_integrare',)
    list_filter = ('cassetta__stato', 'cassetta')
    save_on_top = True


class RilevatoreH2SAdmin(admin.ModelAdmin):
    fields = (
        'uso',
        'lavoratore',
        'marca',
        'matricola',
        'data_scadenza',
        'data_bump_test'
    )
    list_display = ('uso', 'lavoratore', 'marca', 'matricola', 'data_scadenza', 'data_bump_test')
    # list_filter = ('cassetta__stato', 'cassetta')
    save_on_top = True


admin.site.register(Formazione, FormazioneAdmin)
admin.site.register(Non_Conformita, Non_ConformitaAdmin)
admin.site.register(DPI2, DPIAdmin)
admin.site.register(CassettaPS, CassettaPSAdmin)
admin.site.register(VerificaCassettaPS, VerificaCassettaPSAdmin)
admin.site.register(RilevatoreH2S, RilevatoreH2SAdmin)

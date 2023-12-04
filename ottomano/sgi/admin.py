from django.contrib import admin

from .models import Formazione, Non_Conformita, DPI2, CassettaPS, VerificaCassettaPS


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
        'stato',
        'numero',
        'allegato',
        'ubicazione',
        ('messa_in_servizio', 'dismissione'),
        ('scadenza', 'ultima_verifica'),
    )
    list_display = ('stato', 'numero', 'allegato', 'ubicazione', 'ultima_verifica', 'scadenza')
    list_filter = ('stato',)
    save_on_top = True


class VerificaCassettaPSAdmin(admin.ModelAdmin):
    fields = (
        'cassetta',
        'data_verifica',
        'data_scadenza',
        'operazione',
        'note',
    )
    list_display = ('cassetta', 'data_verifica', 'data_scadenza', 'operazione', 'note')
    list_filter = ('cassetta__stato',)
    save_on_top = True


admin.site.register(Formazione, FormazioneAdmin)
admin.site.register(Non_Conformita, Non_ConformitaAdmin)
admin.site.register(DPI2, DPIAdmin)
admin.site.register(CassettaPS, CassettaPSAdmin)
admin.site.register(VerificaCassettaPS, VerificaCassettaPSAdmin)

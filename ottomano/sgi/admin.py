from django.contrib import admin

from .models import Formazione, Non_Conformita, DPI2, CassettaPS, VerificaCassettaPS, RilevatoreH2S, DPI_Anticaduta


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
        ('consegna', 'ck_consegna'),
        ('elmetto', 'elmetto_df', 'ck_elmetto'),
        ('rilevatore', 'ck_rilevatore'),
        ('maschera', 'ck_maschera'),
    )
    list_display = ('lavoratore', 'consegna', 'elmetto', 'rilevatore', 'maschera')
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
    # fields = (
    #     'cassetta',
    #     'data_verifica',
    #     'data_scadenza',
    #     'operazione',
    #     ('materiale_integrato',
    #      'materiale_da_integrare'),
    #     'sc2_guanti',
    #     'sc2_iodio',
    #     'sc2_fisiologica',
    #     'sc2_garza18x40',
    #     'sc2_garza10x10',
    #     'sc2_pinzette',
    #     'sc2_cotone',
    #     'sc2_cerotti',
    #     'sc2_cerotto25',
    #     'sc2_benda10',
    #     'sc2_forbici',
    #     'sc2_laccio',
    #     'sc2_ghiaccio',
    #     'sc2_sacchetto',
    #     'sc2_istruzioni',
    # )
    fieldsets = [
        (None,
         {'fields': [
             'cassetta',
             'data_verifica',
             'data_scadenza',
             'operazione',
             ('materiale_integrato', 'materiale_da_integrare'),
         ]}),

        ('Cassetta All. I',
         {"classes": ["collapse"],
          'fields': [
              'sc1_guanti',
              'sc1_iodio',
              'sc1_fisiologica',
              'sc1_garza10x10',
              'sc1_garza18x40',
              'sc1_pinzette',
              'sc1_cotone',
              'sc1_cerotti',
              'sc1_cerotto25',
              'sc1_visiera',
              'sc1_forbici',
              'sc1_laccio',
              'sc1_ghiaccio',
              'sc1_sacchetto',
              'sc1_teli',
              'sc1_rete',
              'sc1_termometro',
              'sc1_sfigmomanometro',
              'sc1_istruzioni'
          ]}),

        ('Cassetta All. II',
         {"classes": ["collapse"],
          'fields': [
              'sc2_guanti',
              'sc2_iodio',
              'sc2_fisiologica',
              'sc2_garza18x40',
              'sc2_garza10x10',
              'sc2_pinzette',
              'sc2_cotone',
              'sc2_cerotti',
              'sc2_cerotto25',
              'sc2_benda10',
              'sc2_forbici',
              'sc2_laccio',
              'sc2_ghiaccio',
              'sc2_sacchetto',
              'sc2_istruzioni',
          ]}),
    ]
    list_display = ('cassetta', 'data_verifica', 'data_scadenza', 'operazione', 'materiale_integrato',
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


class DPI_AnticadutaAdmin(admin.ModelAdmin):
    # fields = (
    #     'uso',
    #     'lavoratore',
    #     'marca',
    #     'matricola',
    #     'data_scadenza',
    #     'data_bump_test'
    # )
    list_display = (
        'uso', 'lavoratore', 'tipologia', 'tipo', 'marca', 'modello', 'matricola', 'data_fabbricazione',
        'data_messa_in_servizio', 'data_scadenza'
    )
    # list_filter = ('cassetta__stato', 'cassetta')
    save_on_top = True


admin.site.register(Formazione, FormazioneAdmin)
admin.site.register(Non_Conformita, Non_ConformitaAdmin)
admin.site.register(DPI2, DPIAdmin)
admin.site.register(CassettaPS, CassettaPSAdmin)
admin.site.register(VerificaCassettaPS, VerificaCassettaPSAdmin)
admin.site.register(RilevatoreH2S, RilevatoreH2SAdmin)
admin.site.register(DPI_Anticaduta, DPI_AnticadutaAdmin)

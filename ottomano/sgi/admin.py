import datetime

from django.contrib import admin, messages

from .models import Formazione, Formazione_Organico_Medio_Annuo, Non_Conformita, DPI2, CassettaPS, VerificaCassettaPS, \
    RilevatoreH2S, DPI_Anticaduta2, DPI_Anticaduta_Operazione, AccessoriSollevamento, AccessoriSollevamento_Revisione, \
    FormazioneCantieri, FormazioneCantieri_Cantieri, NearMiss

from personale.models import Lavoratore


class FormazioneAdmin(admin.ModelAdmin):
    list_display = ('mese', 'corso', 'data', 'argomento', 'docente', 'ore', 'persone', 'tipologia')
    date_hierarchy = 'data'
    save_on_top = True


class Formazione_Organico_Medio_AnnuoAdmin(admin.ModelAdmin):
    list_display = ('anno', 'valore')
    save_on_top = True


class NonConformitaAdmin(admin.ModelAdmin):
    fields = (
        'data',
        ('emittente', 'area', 'tipologia', 'gravita'),
        ('delimitazioni', 'pdl', 'dpi', 'ordine_pulizia', 'sollevamenti', 'attrezzature', 'guida', 'ponteggio_uso',
         'ponteggio_stato', 'lavori_quota', 'spazi_confinati'),
        ('descrizione', 'trattamento'),
        ('causa', 'azione_correttiva'),
        ('responsabile_trattamento', 'data_completamento', 'data_verifica'),
    )
    date_hierarchy = 'data'
    list_display = (
        'data', 'emittente', 'area', 'tipologia', 'gravita', 'descrizione', 'trattamento', 'causa', 'azione_correttiva'
    )
    list_filter = ('tipologia', 'gravita')

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
        ('scadenza', 'ck_scadenza'),
        'ultima_verifica',
    )
    list_display = ('numero', 'stato', 'allegato', 'ubicazione', 'ultima_verifica', 'scadenza')
    list_filter = ('stato',)
    save_on_top = True


def VerificaCassetta_duplica(modeladmin, request, queryset):
    cassette = []
    for cassetta in queryset:
        cassette.append(cassetta.cassetta)
        cassetta.pk = None
        cassetta.data_verifica = datetime.date.today()
        cassetta.save()

    modeladmin.message_user(
        request,
        f'Verifiche duplicate {cassette}',
        messages.SUCCESS
    )


VerificaCassetta_duplica.short_description = "Duplica verifica cassetta"


class VerificaCassettaPSAdmin(admin.ModelAdmin):
    actions = [VerificaCassetta_duplica, ]
    fieldsets = [
        (None,
         {'fields': [
             'cassetta',
             'data_verifica',
             'data_scadenza',
             'operazione',
             ('materiale_integrato', 'materiale_da_integrare', 'note'),
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
    list_filter = ('cassetta__stato', 'operazione', 'cassetta')
    save_on_top = True


@admin.register(RilevatoreH2S)
class RilevatoreH2SAdmin(admin.ModelAdmin):
    date_hierarchy = 'data_scadenza'
    fields = (
        'uso',
        'lavoratore',
        'marca',
        'matricola',
        'data_scadenza',
        'data_bump_test',
        'data_calibrazione'
    )
    list_display = ('uso', 'lavoratore', 'marca', 'matricola', 'data_scadenza', 'data_bump_test', 'data_calibrazione',)
    list_filter = ('marca', 'uso')
    save_on_top = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Lavoratore.objects.filter(in_forza=True).exclude(cantiere__cantiere='Uffici Sede')

        return super(RilevatoreH2SAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(DPI_Anticaduta_Operazione)
class DPI_Anticaduta_OperazioneAdmin(admin.ModelAdmin):
    list_display = ('data', 'operazione', 'lavoratore')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Lavoratore.objects.filter(in_forza=True).exclude(cantiere__cantiere='Uffici Sede')

        return super(DPI_Anticaduta_OperazioneAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class DPI_AnticadutaAdmin(admin.ModelAdmin):
    fields = ('matricola_interna',
              ('stato', 'lavoratore'),
              'tipologia',
              ('marca', 'modello'),
              ('fabbricazione', 'matricola',),
              ('messa_in_servizio', 'consegna2', 'dismissione'),
              ('data_verifica', 'ck_revisione'),
              'operazione',
              )
    filter_horizontal = ('operazione',)
    list_display = (
        'tipologia', 'matricola_interna', 'stato', 'lavoratore', 'consegna2', 'data_verifica',
        'marca', 'modello', 'fabbricazione', 'matricola', 'messa_in_servizio', 'dismissione'
    )
    list_filter = ('tipologia', 'stato')
    readonly_fields = (
        'stato', 'lavoratore', 'messa_in_servizio', 'dismissione', 'data_verifica', 'ck_revisione', 'consegna2')
    save_on_top = True


@admin.register(AccessoriSollevamento)
class AccessoriSollevamentoAdmin(admin.ModelAdmin):
    fields = (
        ('codice', 'tipo'),
        'marca', 'anno',
        ('portata', 'lunghezza', 'colore'),
        ('terminali', 'diametro'),
        'reparto',
        # ('usura_leggera', 'usura_media', 'usura_grave', 'usura_sostituzione'),  # todo:obsoleto
        ('usura', 'conforme', 'in_uso'),
        'data_messa_in_servizio', 'data_dismissione', 'note', 'stato')
    list_display = (
        'codice', 'tipo', 'marca', 'portata', 'lunghezza', 'colore', 'reparto', 'usura',
        # 'usura_leggera', 'usura_media', 'usura_grave', 'usura_sostituzione',  # todo:obsoleto
        'conforme', 'in_uso', 'data_messa_in_servizio', 'data_dismissione', 'note')
    list_filter = ('in_uso', 'tipo', 'reparto')
    readonly_fields = ('stato',)
    save_on_top = True


@admin.register(FormazioneCantieri)
class FormazioneCantieri_Admin(admin.ModelAdmin):
    fields = (
        ('cantiere', 'attivo'),
        ('tipo', 'tipo_revisione', 'tipo_nome'),
        'ifa_trimestre',
        'lavoratori'
    )
    filter_horizontal = ('lavoratori',)
    list_display = (
        'attivo', 'cantiere', 'nome_documento', 'tipo', 'tipo_revisione', 'tipo_nome', 'ifa_trimestre',)
    list_filter = ('attivo',)
    save_on_top = True

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'lavoratori':
            kwargs["queryset"] = Lavoratore.objects.filter(in_forza=True).exclude(cantiere__cantiere='Uffici Sede')

        return super(FormazioneCantieri_Admin, self).formfield_for_manytomany(db_field, request, **kwargs)


class FormazioneCantieri_Cantieri_Admin(admin.ModelAdmin):
    list_display = ('nome', 'in_corso', 'tipo')


@admin.register(NearMiss)
class NearMiss_Admin(admin.ModelAdmin):
    date_hierarchy = 'data'
    list_display = (
        'data', 'tipologia', 'infortunato', 'descrizione', 'cause')
    list_filter = ('tipologia',)
    save_on_top = True


admin.site.register(Formazione, FormazioneAdmin)
admin.site.register(Formazione_Organico_Medio_Annuo, Formazione_Organico_Medio_AnnuoAdmin)
admin.site.register(Non_Conformita, NonConformitaAdmin)
admin.site.register(DPI2, DPIAdmin)
admin.site.register(CassettaPS, CassettaPSAdmin)
admin.site.register(VerificaCassettaPS, VerificaCassettaPSAdmin)
# admin.site.register(RilevatoreH2S, RilevatoreH2SAdmin)
admin.site.register(DPI_Anticaduta2, DPI_AnticadutaAdmin)
# admin.site.register(DPI_Anticaduta_Operazione, DPI_Anticaduta_OperazioneAdmin)
# admin.site.register(AccessoriSollevamento, AccessoriSollevamentoAdmin)
admin.site.register(AccessoriSollevamento_Revisione)
# admin.site.register(FormazioneCantieri, FormazioneCantieri_Admin)
admin.site.register(FormazioneCantieri_Cantieri, FormazioneCantieri_Cantieri_Admin)

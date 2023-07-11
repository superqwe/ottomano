from django.contrib import admin

from .models import Formazione, Non_Conformita


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


admin.site.register(Formazione, FormazioneAdmin)
admin.site.register(Non_Conformita, Non_ConformitaAdmin)

from django.contrib import admin

from .models import Formazione


class FormazioneAdmin(admin.ModelAdmin):
    list_display = ('mese', 'corso', 'data', 'argomento', 'docente', 'ore', 'persone')
    date_hierarchy = 'data'
    save_on_top = True


admin.site.register(Formazione, FormazioneAdmin)

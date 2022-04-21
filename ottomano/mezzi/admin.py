from django.contrib import admin
from .models import Mezzo, RCT


# Register your models here.

class MezzoAdmin(admin.ModelAdmin):
    list_display = (
        'in_forza', 'tipologia', 'marca', 'modello', 'targa', 'matricola', 'assicurazione', 'libretto',
        'revisione', 'rct_aziendale', 'inail')
    list_display_links = ('in_forza', 'tipologia', 'marca', 'modello', 'targa', 'matricola',)
    list_filter = ('in_forza', 'tipologia')
    save_on_top = True


admin.site.register(Mezzo, MezzoAdmin)
admin.site.register(RCT)

from django.contrib import admin

from .models import Mezzo, RCT


@admin.register(Mezzo)
class MezzoAdmin(admin.ModelAdmin):
    fields = (
        'in_forza',
        ('tipologia', 'marca', 'modello', 'targa', 'matricola'),
        ('ce', 'ce_accessori'),
        ('rct_aziendale', 'assicurazione', 'assicurazione_ck'),
        ('libretto', 'revisione', 'revisione_ck'),
        ('libretto_inail', 'immatricolazione', 'matricola_inail'),
        ('inail', 'inail_ck'),
        'manuale',
        ('scc_verificato', 'scc_numero_verifica'),
        ('scadenza_ap', 'consegnato_ap'),
        'faldone'
    )

    list_display = (
        'in_forza', 'tipologia', 'marca', 'modello', 'targa', 'matricola', 'assicurazione', 'libretto',
        'revisione', 'rct_aziendale', 'inail', 'faldone')
    list_display_links = ('in_forza', 'tipologia', 'marca', 'modello', 'targa', 'matricola',)
    list_filter = ('in_forza', 'tipologia')
    save_on_top = True


admin.site.register(RCT)

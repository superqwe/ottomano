from django.contrib import admin

from .models import Tipologia, Attrezzo


class TipologiaAdmin(admin.ModelAdmin):
    list_display = ('nome',
                    'faldone'
                    )


class AttrezzoAdmin(admin.ModelAdmin):
    def get_faldone(self, obj):
        return obj.tipologia.faldone
    get_faldone.short_description = 'Faldone'
    get_faldone.admin_order_field = 'tipologia__faldone'

    list_display = ('tipologia',
                    'marca',
                    'modello',
                    'matricola',
                    'ce',
                    'manuale',
                    'get_faldone'
                    )
    list_display_links = ('tipologia',
                          'marca',
                          'modello'
                          )
    list_filter = ('tipologia',)
    save_on_top = True


admin.site.register(Tipologia, TipologiaAdmin)
admin.site.register(Attrezzo, AttrezzoAdmin)

from django.contrib import admin

from .models import Tipologia, Attrezzo


class AttrezzoAdmin(admin.ModelAdmin):
    list_display = ('tipologia',
                    'marca',
                    'modello',
                    'matricola',
                    'ce',
                    'manuale',
                    'faldone'
                    )
    list_display_links = ('tipologia',
                          'marca',
                          'modello'
                          )
    list_filter = ('tipologia',)
    save_on_top = True


admin.site.register(Tipologia)
admin.site.register(Attrezzo, AttrezzoAdmin)

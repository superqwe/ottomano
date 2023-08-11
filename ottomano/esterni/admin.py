from django.contrib import admin
from .models import Cantiere_Esterno
from personale.models import Lavoratore
from mezzi.models import Mezzo


class CantiereEsternoAdmin(admin.ModelAdmin):
    filter_horizontal = ['elenco_lavoratori', 'elenco_mezzi']
    list_display = ('in_corso', 'cantiere')
    list_display_links = ('cantiere',)
    list_filter =  ['in_corso',]
    save_on_top = True

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'elenco_lavoratori':
            kwargs["queryset"] = Lavoratore.objects.filter(in_forza=True)

        elif db_field.name == 'elenco_mezzi':
            kwargs["queryset"] = Mezzo.objects.filter(in_forza=True)

        return super(CantiereEsternoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Cantiere_Esterno, CantiereEsternoAdmin)

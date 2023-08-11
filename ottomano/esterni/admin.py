from django.contrib import admin
from .models import Cantiere_Esterno
# from personale import models as personale_models

class CantiereEsternoAdmin(admin.ModelAdmin):
    filter_horizontal = ['elenco_lavoratori',]
    # list_filter =  ['elenco_lavoratori',]
    save_on_top = True

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == 'elenco_lavoratori':
    #         kwargs["queryset"] = personale_models.objects.filter(in_forza=True)
    #     return super(CantiereEsternoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Cantiere_Esterno, CantiereEsternoAdmin)
from django.contrib import admin

from .models import Lavoratore


# Register your models here.

class LavoratoreAdmin(admin.ModelAdmin):
    list_display = ('cognome', 'nome')


admin.site.register(Lavoratore, LavoratoreAdmin)

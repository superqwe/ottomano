from django.db import models
# from personale import models as personale_models
from personale.models import Lavoratore, Formazione
from mezzi.models import Mezzo


class Cantiere_Esterno(models.Model):
    cantiere = models.CharField(max_length=100, blank=True, null=True)
    in_corso = models.BooleanField(default=True)
    elenco_lavoratori = models.ManyToManyField(Lavoratore, blank=True)
    # elenco_lavoratori2 = models.ManyToManyField(Formazione, blank=True)
    elenco_mezzi = models.ManyToManyField(Mezzo, blank=True)

    def __str__(self):
        return self.cantiere

    class Meta:
        ordering = ['cantiere', ]
        verbose_name = 'Cantiere Esterno'
        verbose_name_plural = 'Cantieri Esterni'

from django.db import models
from personale import models as personale_models


class Cantiere_Esterno(models.Model):
    cantiere = models.CharField(max_length=100, blank=True, null=True)
    elenco_lavoratori = models.ManyToManyField(personale_models.Lavoratore)

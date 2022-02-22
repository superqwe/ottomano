from django.db import models


# Create your models here.

class Lavoratore(models.Model):
    in_forza = models.BooleanField(default=True)
    matricola = models.IntegerField(blank=True, null=True)
    cognome = models.CharField(max_length=20, blank=True, null=True)
    nome = models.CharField(max_length=20, blank=True, null=True)
    cf = models.CharField(verbose_name='CF', max_length=16, blank=True, null=True)
    sesso = models.CharField(max_length=1, blank=True, null=True)
    data_nascita = models.DateField(blank=True, null=True)
    luogo_nascita = models.CharField(max_length=30, blank=True, null=True)
    provincia_nascita = models.CharField(max_length=2, blank=True, null=True)
    indirizzo = models.CharField(max_length=50, blank=True, null=True)
    cap = models.CharField(max_length=2, blank=True, null=True)
    citta = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=2, blank=True, null=True)
    cellulare = models.IntegerField(blank=True, null=True)
    tipo_contratto = models.CharField(max_length=20, blank=True, null=True)
    data_inizio = models.DateField(blank=True, null=True)
    data_fine = models.DateField(blank=True, null=True)
    livello = models.CharField(max_length=2, blank=True, null=True)
    qualifica = models.CharField(max_length=20, blank=True, null=True)
    assunzione = models.CharField(max_length=20, blank=True, null=True)
    busta_paga = models.CharField(max_length=20, blank=True, null=True)
    mansione = models.CharField(max_length=20, blank=True, null=True)
    attivita_svolta = models.CharField(max_length=20, blank=True, null=True)
    mansione_1 = models.CharField(max_length=20, blank=True, null=True)
    mansione_2 = models.CharField(max_length=20, blank=True, null=True)
    mansione_3 = models.CharField(max_length=20, blank=True, null=True)
    reparto = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name = 'Lavoratore'
        verbose_name_plural = 'Lavoratori'

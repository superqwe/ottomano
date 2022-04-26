from django.db import models
import datetime

TIPOLOGIA = [
    ('aut', 'Auto'),
    ('auc', 'Autocarro'),
    ('bet', 'Betoniera'),
    ('car', 'Carrello'),
    ('dum', 'Dumper'),
    ('esc', 'Escavatore'),
    ('fur', 'Furgone'),
    ('pal', 'Pala'),
    ('ple', 'PLE'),
    ('rim', 'Rimorchio'),
    ('rul', 'Rullo'),
    ('sol', 'Sollevatore'),
    ('ter', 'Terna'),
]


class RCT(models.Model):
    scadenza = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'RCT Aziendale'
        verbose_name_plural = 'RCT Aziendale'

    def __str__(self):
        return '%s' % self.scadenza


class Mezzo(models.Model):
    in_forza = models.BooleanField(default=True)
    tipologia = models.CharField(max_length=3, choices=TIPOLOGIA, blank=True, null=True, default=None)
    marca = models.CharField(max_length=30, blank=True, null=True, default=None)
    modello = models.CharField(max_length=30, blank=True, null=True, default=None)
    targa = models.CharField(max_length=30, blank=True, null=True, default=None)
    matricola = models.CharField(max_length=30, blank=True, null=True, default=None)
    ce = models.BooleanField(default=False)
    ce_accessori = models.BooleanField(default=False)
    assicurazione = models.DateField(blank=True, null=True)
    rct_aziendale = models.BooleanField(default=False)
    libretto = models.BooleanField(default=None)
    revisione = models.DateField(blank=True, null=True)
    immatricolazione = models.DateField(blank=True, null=True)
    inail = models.DateField(blank=True, null=True)

    def nome(self):
        t_m = self.targa if self.targa else self.matricola
        modello = self.modello.replace('/', '_').replace('.', '_')
        return '%s - %s - %s' % (self.marca, modello, t_m)

    def scadenza_mezzo(self):
        if self.rct_aziendale:
            return 'aziendale'
        else:
            return self.assicurazione

    class Meta:
        ordering = ['tipologia', 'marca', 'modello', 'targa', 'matricola']
        verbose_name = 'Mezzo'
        verbose_name_plural = 'Mezzi'

    def __str__(self):
        return self.nome()

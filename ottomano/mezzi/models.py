from django.db import models

TIPOLOGIA = [
    ('aut', 'Auto'),
    ('fur', 'Furgone'),
    ('esc', 'Escavatore'),
    ('pal', 'Pala'),
    ('ter', 'Terna'),
    ('car', 'Carrello'),
    ('sol', 'Sollevatore'),
    ('ple', 'PLE'),
    ('bet', 'Betoniera'),
    ('dum', 'Dumper'),
    ('rul', 'Rullo'),
]


# Create your models here.
class Mezzo(models.Model):
    in_forza = models.BooleanField(default=True)
    tipologia = models.CharField(max_length=3, choices=TIPOLOGIA, blank=True, null=True, default=None)
    marca = models.CharField(max_length=30, blank=True, null=True, default=None)
    modello = models.CharField(max_length=30, blank=True, null=True, default=None)
    targa = models.CharField(max_length=30, blank=True, null=True, default=None)
    matricola = models.CharField(max_length=30, blank=True, null=True, default=None)
    ce = models.BooleanField(default=True)
    assicurazione = models.DateField(blank=True, null=True)
    rct = models.DateField(blank=True, null=True)
    revisione = models.DateField(blank=True, null=True)
    inail = models.DateField(blank=True, null=True)

    def nome(self):
        t_m = self.targa if self.targa else self.matricola
        return '%s - %s - %s' % (self.marca, self.modello, t_m)

    class Meta:
        ordering = ['tipologia', 'marca', 'modello', 'targa', 'matricola']
        verbose_name = 'Mezzo'
        verbose_name_plural = 'Mezzi'

    def __str__(self):
        return self.nome()

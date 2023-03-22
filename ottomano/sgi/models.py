from django.db import models

MESE = [
    ('01', 'Gennaio'),
    ('02', 'Febbraio'),
    ('03', 'Marzo'),
    ('04', 'Aprile'),
    ('05', 'Maggio'),
    ('06', 'Giugno'),
    ('07', 'Luglio'),
    ('08', 'Agosto'),
    ('09', 'Settembre'),
    ('10', 'Ottobre'),
    ('11', 'Novembre'),
    ('12', 'Dicembre'),
    ('s1', '1° Semestre'),
    ('s2', '2° Semestre'),
]


class Formazione(models.Model):
    mese = models.CharField(max_length=20, choices=MESE, blank=True, null=True)
    corso = models.IntegerField(blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    argomento = models.CharField(max_length=100, blank=True, null=True)
    docente = models.CharField(max_length=20, blank=True, null=True)
    ore = models.CharField(max_length=6, blank=True, null=True)
    persone = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-data', '-corso']
        verbose_name = 'Formazione'
        verbose_name_plural = 'Formazioni'

    def __str__(self):
        return '%s %s' % (self.data, self.argomento)

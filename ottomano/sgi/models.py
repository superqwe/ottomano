from django.db import models

#  FORMAZIONE ---------------------------------------------------------------------------------------------------------
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
    docente = models.CharField(max_length=30, blank=True, null=True)
    ore = models.CharField(max_length=6, blank=True, null=True)
    persone = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-data', '-corso']
        verbose_name = 'Formazione'
        verbose_name_plural = 'Formazioni'

    def __str__(self):
        return '%s %s' % (self.data, self.argomento)


# NON CONFORMITÀ ------------------------------------------------------------------------------------------------------
EMITTENTE = [
    ('sogein', 'CSE SOGEIN'),
    ('scc', 'CSE SCC'),
    ('a_scc', 'Assistente CSE SCC'),
    ('aspp', 'ASPP'),
    ('hse eni', 'HSE ENI'),
    ('a_hse_scc', 'Assistente HSE SCC'),
]
AREA = [
    ('sic', 'Sicurezza'),
]

TIPOLOGIA = [
    ('nc', 'NC'),
]

RESPONSABILE_TRATTAMENTO = [
    ('aspp', 'ASPP'),
]


class Non_Conformita(models.Model):
    data = models.DateField(blank=True, null=True)
    emittente = models.CharField(max_length=10, choices=EMITTENTE, blank=True, null=True)
    area = models.CharField(max_length=10, choices=AREA, blank=True, null=True, default='sic')
    tipologia = models.CharField(max_length=10, choices=TIPOLOGIA, blank=True, null=True, default='nc')
    descrizione = models.TextField(blank=True, null=True)
    trattamento = models.TextField(blank=True, null=True)
    causa = models.TextField(blank=True, null=True)
    azione_correttiva = models.TextField(blank=True, null=True)
    responsabile_trattamento = models.CharField(max_length=10, choices=RESPONSABILE_TRATTAMENTO, blank=True, null=True,
                                                default='aspp')
    data_completamento = models.DateField(blank=True, null=True)
    data_verifica = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Non Conformità'
        verbose_name_plural = 'Non Conformità'

    def __str__(self):
        return 'NC del %s' % (self.data,)

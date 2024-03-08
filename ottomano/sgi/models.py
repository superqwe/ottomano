from django.db import models

from personale.models import Lavoratore

from pprint import pp

STATO_DOCUMENTI = [
    (None, 'ok_np'),
    ('table-warning', 'scade'),
    ('table-danger', 'scaduto')
]

# CASSETTE PS ---------------------------------------------------------------------------------------------------------
ALLEGATO_CASSETTA_PS = [
    ('1', '1'),
    ('2', '2')
]
STATO_CASSETTA_PS = [
    ('0', 'Dismessa'),
    ('-1', 'Da reintegrare'),
    ('1', 'Ok')
]

OPERAZIONE_CASSETTA_PS = [
    ('ok', 'Verificata'),
    ('no', 'Da reintegrare'),
    ('rei', 'Reintegrata'),
    ('dis', 'Dismessa'),
    ('ms', 'Messa in servizio'),
]

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

#  RILEVATORE H2S------------------------------------------------------------------------------------------------------
MARCA_RILEVATORE_H2S = [
    ('hw', 'Honeywell'),
    ('dr', 'Drager'),
    ('ms', 'MSA'),
]
USO_RILEVATORE_H2S = [
    ('l', 'Consegnato'),
    ('f', 'Fornitori'),
    ('d', 'Disponibile')

]

# NON CONFORMITÀ ------------------------------------------------------------------------------------------------------
NC_EMITTENTE = [
    ('sogein', 'CSE SOGEIN'),
    ('scc', 'CSE SCC'),
    ('a_scc', 'Assistente CSE SCC'),
    ('aspp', 'ASPP'),
    ('rsgi', 'RSGI'),
    ('hse eni', 'HSE ENI'),
    ('a_hse_scc', 'Assistente HSE SCC'),
]
NC_AREA = [
    ('sic', 'Sicurezza'),
    ('qua', 'Qualità'),
    ('qhse', 'QHSE'),
]

NC_TIPOLOGIA = [
    ('nc', 'NC'),
    ('oss', 'OSS'),
]

NC_RESPONSABILE_TRATTAMENTO = [
    ('aspp', 'ASPP'),
    ('rsgi', 'RSGI'),
]

# DPI ANTICADUTA ------------------------------------------------------------------------------------------------------
USO_DPI_ANTICADUTA = [
    ('c', 'Consegnato'),
    ('d', 'Disponibile'),
]

TIPOLOGIA_DPI_ANTICADUTA = [
    ('im', 'Imbracatura'),
    ('c1', 'Cordino Singolo'),
    ('c2', 'Cordino Doppio'),
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


class Non_Conformita(models.Model):
    data = models.DateField(blank=True, null=True)
    emittente = models.CharField(max_length=10, choices=NC_EMITTENTE, default='aspp', blank=True, null=True)
    area = models.CharField(max_length=10, choices=NC_AREA, blank=True, null=True, default='sic')
    tipologia = models.CharField(max_length=10, choices=NC_TIPOLOGIA, blank=True, null=True, default='nc')
    descrizione = models.TextField(blank=True, null=True)
    trattamento = models.TextField(blank=True, null=True)
    causa = models.TextField(blank=True, null=True)
    azione_correttiva = models.TextField(blank=True, null=True)
    responsabile_trattamento = models.CharField(max_length=10, choices=NC_RESPONSABILE_TRATTAMENTO, blank=True,
                                                null=True, default='aspp')
    data_completamento = models.DateField(blank=True, null=True)
    data_verifica = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Non Conformità'
        verbose_name_plural = 'Non Conformità'

    def __str__(self):
        return 'NC del %s' % (self.data,)


class DPI2(models.Model):
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE)
    consegna = models.DateField(blank=True, null=True, default=None)
    elmetto = models.DateField(blank=True, null=True, default=None)
    elmetto_df = models.DateField('Data di fabbricazione', blank=True, null=True, default=None)
    rilevatore = models.DateField(blank=True, null=True, default=None)
    maschera = models.DateField(blank=True, null=True, default=None)

    ck_consegna = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_elmetto = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_rilevatore = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_maschera = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')

    class Meta:
        ordering = ['lavoratore', ]
        verbose_name = 'Consegna DPI'
        verbose_name_plural = 'Consegne DPI'

    def __str__(self):
        return '%s %s - %s' % (self.lavoratore.cognome, self.lavoratore.nome, self.consegna)


class CassettaPS(models.Model):
    numero = models.CharField(max_length=10)
    stato = models.CharField(max_length=10, choices=STATO_CASSETTA_PS, blank=True, null=True)
    ubicazione = models.CharField(max_length=30, blank=True, null=True)
    allegato = models.CharField(max_length=10, choices=ALLEGATO_CASSETTA_PS, default='2', blank=True, null=True)
    messa_in_servizio = models.DateField(blank=True, null=True)
    dismissione = models.DateField(blank=True, null=True)
    scadenza = models.DateField(blank=True, null=True)
    ultima_verifica = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['numero', ]
        verbose_name = 'Cassetta PS'
        verbose_name_plural = 'Cassette PS'

    def __str__(self):
        return self.numero


class VerificaCassettaPS(models.Model):
    cassetta = models.ForeignKey(CassettaPS, on_delete=models.CASCADE)
    data_verifica = models.DateField(blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)
    operazione = models.CharField(max_length=10, choices=OPERAZIONE_CASSETTA_PS, blank=True, null=True)
    materiale_integrato = models.TextField('Materiale reintegrato', blank=True, null=True)
    materiale_da_integrare = models.TextField('Materiale da reintegrare', blank=True, null=True)

    sc1_guanti = models.DateField('Guanti sterili', blank=True, null=True)
    sc1_iodio = models.DateField('Iodiopovidone 125ml', blank=True, null=True)
    sc1_fisiologica = models.DateField('Fisiologica 250ml', blank=True, null=True)
    sc1_garza10x10 = models.DateField('Garza 10x10', blank=True, null=True)
    sc1_garza18x40 = models.DateField('Garza 18x40', blank=True, null=True)
    sc1_pinzette = models.DateField('Pinzette', blank=True, null=True)
    sc1_cotone = models.DateField('Cotone idrofilo', blank=True, null=True)
    sc1_cerotti = models.DateField('Cerotti', blank=True, null=True)
    sc1_cerotto25 = models.DateField('Cerotto alto 2.5cm', blank=True, null=True)
    sc1_visiera = models.DateField('Visiera paraschizzi', blank=True, null=True)
    sc1_forbici = models.BooleanField('Forbici', blank=True, null=True)
    sc1_laccio = models.DateField('Laccio emostatico', blank=True, null=True)
    sc1_ghiaccio = models.DateField('Ghiaccio pronto uso', blank=True, null=True)
    sc1_sacchetto = models.BooleanField('Sacchetto monouso', blank=True, null=True)
    sc1_teli = models.DateField('Teli sterili', blank=True, null=True)
    sc1_rete = models.DateField('Rete elastica', blank=True, null=True)
    sc1_termometro = models.BooleanField('termometro', blank=True, null=True)
    sc1_sfigmomanometro = models.BooleanField('Sfigmomanometro', blank=True, null=True)
    sc1_istruzioni = models.BooleanField('Istruzioni/Estratto DLgs 81/08', blank=True, null=True)

    sc2_guanti = models.DateField('Guanti sterili', blank=True, null=True)
    sc2_iodio = models.DateField('Iodiopovidone 125ml', blank=True, null=True)
    sc2_fisiologica = models.DateField('Fisiologica 250ml', blank=True, null=True)
    sc2_garza18x40 = models.DateField('Garza 18x40', blank=True, null=True)
    sc2_garza10x10 = models.DateField('Garza 10x10', blank=True, null=True)
    sc2_pinzette = models.DateField('Pinzette', blank=True, null=True)
    sc2_cotone = models.DateField('Cotone idrofilo', blank=True, null=True)
    sc2_cerotti = models.DateField('Cerotti', blank=True, null=True)
    sc2_cerotto25 = models.DateField('Cerotto alto 2.5cm', blank=True, null=True)
    sc2_benda10 = models.DateField('Benda orlata 10cm', blank=True, null=True)
    sc2_forbici = models.BooleanField('Forbici', blank=True, null=True)
    sc2_laccio = models.DateField('Laccio emostatico', blank=True, null=True)
    sc2_ghiaccio = models.DateField('Ghiaccio pronto uso', blank=True, null=True)
    sc2_sacchetto = models.BooleanField('Sacchetto monouso', blank=True, null=True)
    sc2_istruzioni = models.BooleanField('Istruzioni/Estratto DLgs 81/08', blank=True, null=True)

    class Meta:
        ordering = ['cassetta', '-data_verifica']
        verbose_name = 'Verifica cassetta PS'
        verbose_name_plural = 'Verifiche cassette PS'

    def __str__(self):
        return '{} {}'.format(self.cassetta, self.data_verifica)


class RilevatoreH2S(models.Model):
    uso = models.CharField(max_length=1, choices=USO_RILEVATORE_H2S, blank=True, null=True)
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE, blank=True, null=True)
    marca = models.CharField(max_length=3, choices=MARCA_RILEVATORE_H2S, blank=True, null=True)
    matricola = models.CharField(max_length=20, blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)
    data_bump_test = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-uso', 'lavoratore']
        verbose_name = 'Rilevatore H2S'
        verbose_name_plural = 'Rilevatori H2S'

    def __str__(self):
        return '{} {}'.format(self.marca, self.matricola)


class DPI_Anticaduta(models.Model):
    uso = models.CharField(max_length=1, choices=USO_DPI_ANTICADUTA, blank=True, null=True)
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE, blank=True, null=True)
    tipologia = models.CharField(max_length=2, choices=TIPOLOGIA_DPI_ANTICADUTA, blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    marca = models.CharField(max_length=20, blank=True, null=True)
    modello = models.CharField(max_length=20, blank=True, null=True)
    matricola = models.CharField(max_length=20, blank=True, null=True)
    data_fabbricazione = models.DateField(blank=True, null=True)
    data_messa_in_servizio = models.DateField(blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-uso', 'lavoratore']
        verbose_name = 'DPI Anticaduta'
        verbose_name_plural = 'DPI Anticaduta'

    def __str__(self):
        return '{} {} {}'.format(self.tipologia, self.marca, self.matricola)

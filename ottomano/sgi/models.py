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
RILEVATORE_H2S_MARCA = [
    ('hw', 'Honeywell'),
    ('dr', 'Drager'),
    ('ms', 'MSA'),
]
RILEVATORE_H2S_USO = [
    ('l', 'Consegnato'),
    ('f', 'Fornitori'),
    ('d', 'Disponibile'),
    ('m', 'Multigas'),
    ('x', 'Dismesso'),
]
RILEVATORE_H2S_STATO = [
    (None, 'ok_np'),
    ('table-warning', 'in scadenza'),
    ('table-danger', 'scaduto')
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
    ('amb', 'Ambiente'),
]

NC_TIPOLOGIA = [
    ('nc', 'NC'),
    ('oss', 'OSS'),
]

NC_RESPONSABILE_TRATTAMENTO = [
    ('aspp', 'ASPP'),
    ('rsgi', 'RSGI'),
]

NC_GRAVITA = [
    ('1', 'Grigia'),
    ('2', 'Gialla'),
    ('3', 'Rossa'),
]

# ACCESSORI_SOLLEVAMENTO -----------------------------------------------------------------------------------------------
ACCESSORI_SOLLEVAMENTO_TIPO = [
    ('car', 'Carrucola'),
    ('cat2', 'Tirante in catena a 2 bracci'),
    ('cat4', 'Tirante in catena a 4 bracci'),
    ('f', 'Braca fibra sintetica piatta'),
    ('fa', 'Braca fibra sintetica piatta ad anello'),
    ('fc', 'Braca fibra sintetica piatta con cricchetto'),
    ('grd', 'Grilli di sollevamento dritti'),
    ('grl', 'Grilli di sollevamento a lira'),
    ('gs', 'Gancio di sollevamento'),
    ('pc', 'Pinze di sollevamento casseri'),
    ('pr', 'Pinze di sollevamento cordoli'),
    ('pl', 'Pinze di sollevamento lamiere'),
    ('pp', 'Pinze di sollevamento pozzetti'),
]

ACCESSORI_SOLLEVAMENTO_DIAMETRO = [
    ('12', '12mm'),
    ('20', '20mm'),
    ('23', '23mm'),
    ('26', '26mm'),
    ('32', '32mm'),
    ('1_2', '1/2"'),
    ('3_4', '3/4"'),
    ('5_8', '5/8"'),
    ('7/8', '7/8"'),
    ('1__1_4', '1+1/4"'),
]

ACCESSORI_SOLLEVAMENTO_COLORE = [
    ('a', 'Arancione'),
    ('b', 'Blu'),
    ('g', 'Giallo'),
    ('gr', 'Grigio'),
    ('m', 'Marrone'),
    ('r', 'Rosso'),
    ('v', 'Verde'),
]

ACCESSORI_SOLLEVAMENTO_TERMINALI = [
    ('an', 'Anello'),
    ('as', 'Asola'),
    ('ga', 'Gancio')
]

ACCESSORI_SOLLEVAMENTO_REVISIONE = [
    ('1', 'I'),
    ('2', 'II'),
    ('3', 'III'),
    ('4', 'IV')
]

ACCESSORI_SOLLEVAMENTO_STATO = [
    ('recente', 'table-success'),
    ('ok', ''),
    ('dismessa_recente', 'table-danger'),
    ('dismessa', 'table-danger'),
]

ACCESSORI_SOLLEVAMENTO_USURA = [
    ('0', 'ok'),
    ('1', 'leggero'),
    ('2', 'medio'),
    ('3', 'grave'),
]


# DPI ANTICADUTA -------------------------------------------------------------------------------------------------------

DPI_ANTICADUTA_STATO = [
    ('c', 'Consegnato'),
    ('d', 'Disponibile'),
    ('v', 'Riconsegnato per verifica'),
    ('vi', 'In Verifica'),
    ('vd', 'Verificata da riconsegnare'),
    ('x', 'Dismesso'),
]
DPI_ANTICADUTA_TIPOLOGIA = [
    ('im', 'Imbracatura'),
    ('c1', 'Cordino Singolo'),
    ('c2', 'Cordino Doppio'),
]

DPI_ANTICADUTA_OPERAZIONE = [
    ('ms', 'Messa in servizio'),
    ('c', 'Consegnato'),
    ('d', 'Riconsegna/Disponibile'),
    ('rv', 'Riconsegna per Verifica'),
    ('vi', 'In Verifica'),
    ('v', 'Verifica'),
    ('x', 'Dismesso'),
]

# FORMAZIONE CANTIERI --------------------------------------------------------------------------------------------------
FORMAZIONE_CANTIERI_CANTIERE_TIPO = (
    ('0', 'DUVRI'),
    ('1', 'TITOLO IV (sotto Coordinamento)'),
    ('2', 'Cantieri Esterni'),
)

FORMAZIONE_CANTIERI_TIPO = (
    ('0', 'IFA'),
    ('1', 'PSC'),
    ('2', 'POS'),
    ('3', 'Altro')
)

FORMAZIONE_CANTIERI_IFA_TRIMESTRE = (
    ('1', 'I'),
    ('2', 'II'),
    ('3', 'III'),
    ('4', 'IV'),
)

# FORMAZIONE _________--------------------------------------------------------------------------------------------------
FORMAZIONE_TIPOLOGIA = (
    ('ifa', 'IFA'),
    ('obb', 'Obblighi legge'),
    ('tiv', 'Cantieri Titolo IV'),
    ('scc', 'Patto Sicurezza'),
    ('sgi', 'SGI'),
)

# NEAR MISS ----------------------------------------------------------------------------------------------------------
NEARMISS_TIPOLOGIA = (
    ('nm', 'Near Miss'),
    ('med', 'Medicazione'),
    ('inf', 'Infortunio'),
    ('inc', 'Incidente'),
)


class FormazioneCantieri_Cantieri(models.Model):
    tipo = models.CharField(max_length=1, choices=FORMAZIONE_CANTIERI_CANTIERE_TIPO, blank=True, null=True)
    nome = models.CharField(max_length=20, blank=True, null=True)
    in_corso = models.BooleanField(default=True, blank=True)

    class Meta:
        ordering = ['tipo', 'nome', ]
        verbose_name = 'Formazione Cantiere - Cantiere'
        verbose_name_plural = 'Formazione Cantiere - Cantieri'

    def __str__(self):
        return '{}'.format(self.nome)


class FormazioneCantieri(models.Model):
    attivo = models.BooleanField(default=True)
    cantiere = models.ForeignKey(FormazioneCantieri_Cantieri, on_delete=models.CASCADE, blank=True, null=True)
    tipo = models.CharField(max_length=1, choices=FORMAZIONE_CANTIERI_TIPO, blank=True, null=True)
    tipo_nome = models.CharField('Nome altro tipo', max_length=20, blank=True, null=True)
    tipo_revisione = models.IntegerField('Revisione', blank=True, null=True)
    ifa_trimestre = models.CharField(max_length=1, choices=FORMAZIONE_CANTIERI_IFA_TRIMESTRE, blank=True, null=True)
    lavoratori = models.ManyToManyField(Lavoratore, blank=True)

    def nome_documento(self):
        match self.tipo:
            case '0':
                return '{}'.format(self.get_ifa_trimestre_display(), )
            case '1':
                return 'PSC {}'.format(self.tipo_revisione, )
            case '2':
                if self.tipo_revisione is not None:
                    return 'POS {}'.format(self.tipo_revisione, )
                else:
                    return 'POS'
            case '3':
                if self.tipo_revisione is None:
                    return '{}'.format(self.tipo_nome, )
                else:
                    return '{} {}'.format(self.tipo_nome, self.tipo_revisione)

    class Meta:
        ordering = ['cantiere', 'tipo', 'tipo_revisione', 'ifa_trimestre']
        verbose_name = 'Formazione Cantiere'
        verbose_name_plural = 'Formazione Cantiere'

    def __str__(self):
        return '{} - {} rev.{}'.format(self.cantiere, self.get_tipo_display(), self.tipo_revisione)


class DPI_Anticaduta_Operazione(models.Model):
    data = models.DateField(blank=True, null=True)
    operazione = models.CharField(max_length=2, choices=DPI_ANTICADUTA_OPERAZIONE, blank=True, null=True)
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['data', 'pk', 'lavoratore']
        verbose_name = 'DPI Anticaduta - Operazione'
        verbose_name_plural = 'DPI Anticaduta - Operazioni'

    def __str__(self):
        lavoratore = self.lavoratore if self.lavoratore else ''
        return '{} {} - {}'.format(self.data, self.get_operazione_display(), lavoratore)


class DPI_Anticaduta2(models.Model):
    matricola_interna = models.IntegerField('ID', blank=True, null=True)
    stato = models.CharField(max_length=2, choices=DPI_ANTICADUTA_STATO, blank=True, null=True)
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE, blank=True, null=True)
    tipologia = models.CharField(max_length=2, choices=DPI_ANTICADUTA_TIPOLOGIA, blank=True, null=True)
    marca = models.CharField(max_length=20, blank=True, null=True)
    modello = models.CharField(max_length=20, blank=True, null=True)
    fabbricazione = models.DateField(blank=True, null=True)
    matricola = models.IntegerField(blank=True, null=True)
    messa_in_servizio = models.DateField(blank=True, null=True)
    dismissione = models.DateField(blank=True, null=True)
    data_verifica = models.DateField('Data ultima verifica', blank=True, null=True)
    operazione = models.ManyToManyField(DPI_Anticaduta_Operazione, blank=True)
    consegna2 = models.DateField('Ultima operazione', blank=True, null=True)
    ck_revisione = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')

    def save(self, *args, **kwargs):
        try:
            for operazione in self.operazione.all():
                self.consegna2 = operazione.data

                match operazione.operazione:
                    case 'ms':
                        # print(operazione.data, 'consegnato - messo in servizio')
                        self.messa_in_servizio = operazione.data
                        self.lavoratore = operazione.lavoratore
                        self.stato = 'c'
                    case 'c':
                        # print(operazione.data, 'consegnato')
                        self.lavoratore = operazione.lavoratore
                        self.stato = 'c'
                    case 'd':
                        # print(operazione.data, 'riconsegnato disponibile in ufficio')
                        self.lavoratore = None
                        self.stato = 'd'
                    case 'rv':
                        # print(operazione.data, 'riconsegnato per verifica')
                        self.lavoratore = operazione.lavoratore
                        self.stato = 'v'
                    case 'vi':
                        # print(operazione.data, 'in verifica')
                        self.stato = 'vi'
                    case 'v':
                        # print(operazione.data, 'verificato')
                        self.data_verifica = operazione.data
                        self.stato = 'vd'
                    case 'x':
                        # print(operazione.data, 'dismesso')
                        self.dismissione = operazione.data
                        self.lavoratore = operazione.lavoratore
                        self.stato = 'x'

        except ValueError:
            print('*** DPI Anticaduta - primo salvataggio')

        try:
            if not self.operazione.all():
                self.lavoratore = None
                self.stato = 'd'

        except ValueError:
            print('*** DPI Anticaduta - primo salvataggio')

        super(DPI_Anticaduta2, self).save(*args, **kwargs)

    def modello_completo(self):
        return '%s %s' % (self.marca, self.modello)

    class Meta:
        ordering = ['-tipologia', 'stato', 'matricola_interna']
        verbose_name = 'DPI Anticaduta'
        verbose_name_plural = 'DPI Anticaduta'

    def __str__(self):
        return '{} {} {}'.format(self.tipologia, self.modello, self.matricola)


class AccessoriSollevamento(models.Model):
    stato = models.CharField(max_length=16, choices=ACCESSORI_SOLLEVAMENTO_STATO, blank=True, null=True)
    tipo = models.CharField(max_length=4, choices=ACCESSORI_SOLLEVAMENTO_TIPO, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    anno = models.IntegerField('Anno Produzione', blank=True, null=True)
    codice = models.CharField(max_length=10, blank=True, null=True)
    diametro = models.CharField(max_length=6, choices=ACCESSORI_SOLLEVAMENTO_DIAMETRO, blank=True, null=True)
    colore = models.CharField(max_length=2, choices=ACCESSORI_SOLLEVAMENTO_COLORE, blank=True, null=True)
    lunghezza = models.CharField(max_length=10, blank=True, null=True)
    portata = models.CharField(max_length=10, blank=True, null=True)
    terminali = models.CharField(max_length=2, choices=ACCESSORI_SOLLEVAMENTO_TERMINALI, blank=True, null=True)
    reparto = models.CharField(max_length=20, blank=True, null=True)
    usura = models.CharField(max_length=2, choices=ACCESSORI_SOLLEVAMENTO_USURA, blank=True, null=True)
    usura_leggera = models.BooleanField(blank=True, null=True) # todo:obsoleto
    usura_media = models.BooleanField(blank=True, null=True) # todo:obsoleto
    usura_grave = models.BooleanField(blank=True, null=True) # todo:obsoleto
    # usura_sostituzione = models.BooleanField('Sostituzione', blank=True, null=True)  # todo:obsoleto
    conforme = models.BooleanField(default=True)
    in_uso = models.BooleanField(default=True)
    data_messa_in_servizio = models.DateField(blank=True, null=True)
    data_dismissione = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['codice']
        verbose_name = 'Accessorio di Sollevamento'
        verbose_name_plural = 'Accessori di Sollevamento'

    def __str__(self):
        return '%s - %s' % (self.codice, self.portata)


class AccessoriSollevamento_Revisione(models.Model):
    data_compilazione = models.DateField(blank=True, null=True)
    revisione = models.IntegerField(blank=True, null=True)
    trimestre = models.CharField(max_length=1, choices=ACCESSORI_SOLLEVAMENTO_REVISIONE, blank=True, null=True)
    anno = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Accessori di Sollevamento - Revisione'
        verbose_name_plural = 'Accessori di Sollevamento - Revisioni'

    def __str__(self):
        return 'Revisione %s del %s - Trimestre %s/%s' % (
            self.revisione, self.data_compilazione, self.get_trimestre_display(), self.anno)


class Formazione(models.Model):
    mese = models.CharField(max_length=20, choices=MESE, blank=True, null=True)
    corso = models.IntegerField(blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    argomento = models.CharField(max_length=200, blank=True, null=True)
    docente = models.CharField(max_length=30, blank=True, null=True)
    ore = models.CharField(max_length=6, blank=True, null=True)
    persone = models.IntegerField(blank=True, null=True)
    tipologia = models.CharField(max_length=20, choices=FORMAZIONE_TIPOLOGIA, blank=True, null=True)

    class Meta:
        ordering = ['-data', '-corso']
        verbose_name = 'Formazione'
        verbose_name_plural = 'Formazioni'

    def __str__(self):
        return '%s %s' % (self.data, self.argomento)


class Formazione_Organico_Medio_Annuo(models.Model):
    anno = models.IntegerField(blank=True, null=True)
    valore = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-anno']
        verbose_name = 'Formazione - Organico Medio Annuo'
        verbose_name_plural = 'Formazioni - Organico Medio Annuo'

    def __str__(self):
        return 'Formazione - Organico Medio Annuo del %i: %i' % (self.anno, self.valore)


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

    delimitazioni = models.BooleanField(default=False)
    pdl = models.BooleanField(default=False)
    dpi = models.BooleanField(default=False)
    ordine_pulizia = models.BooleanField(default=False)
    sollevamenti = models.BooleanField(default=False)
    attrezzature = models.BooleanField(default=False)
    guida = models.BooleanField(default=False)
    ponteggio = models.BooleanField(default=False)
    ponteggio_uso = models.BooleanField(default=False)
    ponteggio_stato = models.BooleanField(default=False)
    lavori_quota = models.BooleanField(default=False)
    spazi_confinati = models.BooleanField(default=False)
    gravita = models.CharField(max_length=10, choices=NC_GRAVITA, blank=True, null=True)

    def elenco_tipologia_violazioni(self):
        si_no = (self.delimitazioni, self.pdl, self.dpi, self.ordine_pulizia, self.sollevamenti,
                 self.attrezzature, self.guida, self.ponteggio_uso or self.ponteggio_stato, self.lavori_quota,
                 self.spazi_confinati)
        violazione = ('Delimitazioni', 'PdL', 'DPI', 'Ordine/Pulizia', 'Sollevamenti',
                      'Attrezzature', 'Guida', 'Ponteggio', 'Lavori in Quota', 'Spazi Confinati')

        elenco = [v for sn, v in zip(si_no, violazione) if sn]
        elenco = ', '.join(elenco)

        return elenco

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
    imbracatura = models.DateField(blank=True, null=True, default=None)
    cordino_singolo = models.DateField(blank=True, null=True, default=None)
    cordino_doppio = models.DateField(blank=True, null=True, default=None)

    ck_consegna = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_elmetto = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_rilevatore = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_rilevatore_calibrazione = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True,
                                                  default='ok_np')
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

    ck_scadenza = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')

    class Meta:
        ordering = ['numero', ]
        verbose_name = 'Cassetta PS'
        verbose_name_plural = 'Cassette PS - Elenco'

    def __str__(self):
        return self.numero


class VerificaCassettaPS(models.Model):
    cassetta = models.ForeignKey(CassettaPS, on_delete=models.CASCADE)
    data_verifica = models.DateField(blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)
    operazione = models.CharField(max_length=10, choices=OPERAZIONE_CASSETTA_PS, blank=True, null=True)
    materiale_integrato = models.TextField('Materiale reintegrato', blank=True, null=True)
    materiale_da_integrare = models.TextField('Materiale da reintegrare', blank=True, null=True)
    note = models.TextField('Note', blank=True, null=True)

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

    ck_sc1_guanti = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_iodio = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_fisiologica = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True,
                                          default='ok_np')
    ck_sc1_garza10x10 = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_garza18x40 = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_pinzette = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_cotone = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_cerotti = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_cerotto25 = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_visiera = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_forbici = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_laccio = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_ghiaccio = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_sacchetto = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_teli = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_rete = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_termometro = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc1_sfigmomanometro = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True,
                                              default='ok_np')
    ck_sc1_istruzioni = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')

    ck_sc2_guanti = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_iodio = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_fisiologica = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True,
                                          default='ok_np')
    ck_sc2_garza18x40 = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_garza10x10 = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_pinzette = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_cotone = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_cerotti = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_cerotto25 = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_benda10 = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_forbici = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_laccio = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_ghiaccio = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_sacchetto = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ck_sc2_istruzioni = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')

    class Meta:
        ordering = ['cassetta', '-data_verifica']
        verbose_name = 'Cassetta PS - Verifica'
        verbose_name_plural = 'Cassetta PS - Verifiche'

    def __str__(self):
        return '{} {}'.format(self.cassetta, self.data_verifica)


class RilevatoreH2S(models.Model):
    uso = models.CharField(max_length=1, choices=RILEVATORE_H2S_USO, blank=True, null=True)
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE, blank=True, null=True)
    marca = models.CharField(max_length=3, choices=RILEVATORE_H2S_MARCA, blank=True, null=True)
    matricola = models.CharField(max_length=20, blank=True, null=True)
    data_scadenza = models.DateField(blank=True, null=True)
    data_calibrazione = models.DateField(blank=True, null=True)
    data_bump_test = models.DateField(blank=True, null=True)

    data_calibrazione_ck = models.CharField(max_length=15, choices=RILEVATORE_H2S_STATO, blank=True, null=True)

    class Meta:
        ordering = ['uso', 'lavoratore', 'matricola']
        verbose_name = 'Rilevatore H2S'
        verbose_name_plural = 'Rilevatori H2S'

    def __str__(self):
        return '{} {}'.format(self.get_marca_display(), self.matricola)


class NearMiss(models.Model):
    data = models.DateField(blank=True, null=True)
    tipologia = models.CharField(max_length=3, choices=NEARMISS_TIPOLOGIA, blank=True, null=True)
    infortunato = models.CharField(max_length=50, blank=True, null=True)
    descrizione = models.TextField("Descrizione dell'evento", blank=True, null=True)
    cause = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-data', ]
        verbose_name = 'MIP'
        verbose_name_plural = 'MIP'

    def __str__(self):
        return '{} {}'.format(self.data, self.get_tipologia_display())

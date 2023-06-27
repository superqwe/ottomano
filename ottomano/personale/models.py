from django.db import models

STATO_DOCUMENTI = [
    (None, 'ok_np'),
    ('table-warning', 'scade'),
    ('table-danger', 'scaduto')
]

STATO_FORMAZIONE = [
    ('verde', 'ok'),
    ('giallo', 'scade'),
    ('rosso', 'scaduto')
]


class Cantiere(models.Model):
    cantiere = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['cantiere', ]
        verbose_name = 'Cantiere'
        verbose_name_plural = 'Cantieri'

    def __str__(self):
        return '%s' % self.cantiere


class Lavoratore(models.Model):
    in_forza = models.BooleanField(default=True)
    cantiere = models.ForeignKey(Cantiere, on_delete=models.CASCADE, blank=True, null=True)
    matricola = models.IntegerField(blank=True, null=True)
    cognome = models.CharField(max_length=20, blank=True, null=True)
    nome = models.CharField(max_length=30, blank=True, null=True)
    cf = models.CharField(verbose_name='CF', max_length=16, blank=True, null=True)
    sesso = models.CharField(max_length=1, blank=True, null=True)
    data_nascita = models.DateField(blank=True, null=True)
    luogo_nascita = models.CharField(max_length=30, blank=True, null=True)
    provincia_nascita = models.CharField(max_length=20, blank=True, null=True)
    indirizzo = models.CharField(max_length=50, blank=True, null=True)
    cap = models.IntegerField(blank=True, null=True)
    citta = models.CharField(max_length=50, blank=True, null=True)
    provincia = models.CharField(max_length=20, blank=True, null=True)
    cellulare = models.IntegerField(blank=True, null=True)
    tipo_contratto = models.CharField(max_length=20, blank=True, null=True)
    data_inizio = models.DateField(blank=True, null=True)
    data_fine = models.DateField(blank=True, null=True)
    livello = models.CharField(max_length=2, blank=True, null=True)
    qualifica = models.CharField(max_length=20, blank=True, null=True)
    assunzione = models.CharField(max_length=20, blank=True, null=True)
    busta_paga = models.CharField(max_length=30, blank=True, null=True)
    mansione = models.CharField(max_length=30, blank=True, null=True)
    attivita_svolta = models.CharField(max_length=30, blank=True, null=True)
    mansione_1 = models.CharField(max_length=30, blank=True, null=True)
    mansione_2 = models.CharField(max_length=30, blank=True, null=True)
    mansione_3 = models.CharField(max_length=30, blank=True, null=True)
    reparto = models.CharField(max_length=50, blank=True, null=True)  # todo da rimuovere

    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name = 'Lavoratore'
        verbose_name_plural = 'Lavoratori'

    def __str__(self):
        return '%s %s' % (self.cognome, self.nome)


class Formazione(models.Model):
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE)
    stato = models.CharField(max_length=20, choices=STATO_FORMAZIONE, blank=True, null=True, default='ok_np')
    dirigente = models.DateField(blank=True, null=True, default=None)
    preposto = models.DateField(blank=True, null=True, default=None)
    primo_soccorso = models.DateField(blank=True, null=True, default=None)
    antincendio = models.DateField(blank=True, null=True, default=None)
    art37 = models.DateField(blank=True, null=True, default=None)
    spazi_confinati = models.DateField(blank=True, null=True, default=None)
    ponteggiatore = models.DateField(blank=True, null=True, default=None)
    imbracatore = models.DateField(blank=True, null=True, default=None)
    ept = models.DateField(blank=True, null=True, default=None)
    dumper = models.DateField(blank=True, null=True, default=None)
    rullo = models.DateField(blank=True, null=True, default=None)
    autogru = models.DateField(blank=True, null=True, default=None)
    gru_autocarro = models.DateField(blank=True, null=True, default=None)
    carrello = models.DateField(blank=True, null=True, default=None)
    sollevatore = models.DateField(blank=True, null=True, default=None)
    ple = models.DateField(blank=True, null=True, default=None)
    rls = models.DateField(blank=True, null=True, default=None)
    aspp = models.DateField(blank=True, null=True, default=None)
    nomina_preposto = models.DateField(blank=True, null=True, default=None)
    nomina_preposto_subappalti = models.DateField(blank=True, null=True, default=None)
    nomina_preposto_imbracatore = models.DateField(blank=True, null=True, default=None)
    nomina_antincendio = models.DateField(blank=True, null=True, default=None)
    nomina_primo_soccorso = models.DateField(blank=True, null=True, default=None)
    nomina_aspp = models.DateField(blank=True, null=True, default=None)

    dirigente_dc = models.DateField(blank=True, null=True, default=None)
    preposto_dc = models.DateField(blank=True, null=True, default=None)
    primo_soccorso_dc = models.DateField(blank=True, null=True, default=None)
    antincendio_dc = models.DateField(blank=True, null=True, default=None)
    art37_dc = models.DateField(blank=True, null=True, default=None)
    spazi_confinati_dc = models.DateField(blank=True, null=True, default=None)
    ponteggiatore_dc = models.DateField(blank=True, null=True, default=None)
    imbracatore_dc = models.DateField(blank=True, null=True, default=None)
    ept_dc = models.DateField(blank=True, null=True, default=None)
    dumper_dc = models.DateField(blank=True, null=True, default=None)
    rullo_dc = models.DateField(blank=True, null=True, default=None)
    autogru_dc = models.DateField(blank=True, null=True, default=None)
    gru_autocarro_dc = models.DateField(blank=True, null=True, default=None)
    carrello_dc = models.DateField(blank=True, null=True, default=None)
    sollevatore_dc = models.DateField(blank=True, null=True, default=None)
    ple_dc = models.DateField(blank=True, null=True, default=None)
    rls_dc = models.DateField(blank=True, null=True, default=None)
    aspp_dc = models.DateField(blank=True, null=True, default=None)

    dirigente_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    preposto_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    primo_soccorso_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    antincendio_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    art37_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    spazi_confinati_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True,
                                          default='ok_np')
    ponteggiatore_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    imbracatore_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ept_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    dumper_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    rullo_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    autogru_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    gru_autocarro_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    carrello_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    sollevatore_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    ple_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    rls_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')
    aspp_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')

    class Meta:
        ordering = ['lavoratore', ]
        verbose_name = 'Formazione'
        verbose_name_plural = 'Formazione'

    def __str__(self):
        return '%s %s' % (self.lavoratore.cognome, self.lavoratore.nome)


class Idoneita(models.Model):
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE)
    idoneita = models.DateField(blank=True, null=True, default=None)
    otoprotettori = models.BooleanField(default=False)
    rumore50 = models.BooleanField(default=False)
    guanti = models.BooleanField(default=False)
    posture = models.BooleanField(default=False)
    carichi_10 = models.BooleanField(default=False)
    carichi_15 = models.BooleanField(default=False)
    sollecitazioni_arto_superiore_sinistro = models.BooleanField(default=False)
    spazi_confinati = models.BooleanField(default=False)
    mansioni_gravose = models.BooleanField(default=False)
    temperature = models.BooleanField(default=False)
    scale = models.BooleanField(default=False)
    calzature = models.BooleanField(default=False)
    lenti = models.BooleanField(default=False)

    idoneita_ck = models.CharField(max_length=20, choices=STATO_DOCUMENTI, blank=True, null=True, default='ok_np')

    class Meta:
        ordering = ['lavoratore', ]
        verbose_name = 'Idoneità'
        verbose_name_plural = 'Idoneità'

    def __str__(self):
        return '%s %s - %s' % (self.lavoratore.cognome, self.lavoratore.nome, self.idoneita)

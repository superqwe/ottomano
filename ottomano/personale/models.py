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
    busta_paga = models.CharField(max_length=20, blank=True, null=True)
    mansione = models.CharField(max_length=20, blank=True, null=True)
    attivita_svolta = models.CharField(max_length=20, blank=True, null=True)
    mansione_1 = models.CharField(max_length=20, blank=True, null=True)
    mansione_2 = models.CharField(max_length=20, blank=True, null=True)
    mansione_3 = models.CharField(max_length=20, blank=True, null=True)
    reparto = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['cognome', 'nome']
        verbose_name = 'Lavoratore'
        verbose_name_plural = 'Lavoratori'

    def __str__(self):
        return '%s %s' % (self.cognome, self.nome)


class Formazione(models.Model):
    lavoratore = models.ForeignKey(Lavoratore, on_delete=models.CASCADE)
    preposto = models.DateField(blank=True, null=True, default=None)
    preposto_ck = models.BooleanField(blank=True, null=True, default=None)
    primo_soccorso = models.DateField(blank=True, null=True, default=None)
    primo_soccorso_ck = models.BooleanField(blank=True, null=True, default=None)
    antincendio = models.DateField(blank=True, null=True, default=None)
    antincendio_ck = models.BooleanField(blank=True, null=True, default=None)
    art37 = models.DateField(blank=True, null=True, default=None)
    art37_ck = models.BooleanField(blank=True, null=True, default=None)
    spazi_confinati = models.DateField(blank=True, null=True, default=None)
    spazi_confinati_ck = models.BooleanField(blank=True, null=True, default=None)
    ponteggiatore = models.DateField(blank=True, null=True, default=None)
    ponteggiatore_ck = models.BooleanField(blank=True, null=True, default=None)
    imbracatore = models.DateField(blank=True, null=True, default=None)
    imbracatore_ck = models.BooleanField(blank=True, null=True, default=None)
    ept = models.DateField(blank=True, null=True, default=None)
    ept_ck = models.BooleanField(blank=True, null=True, default=None)
    autogru = models.DateField(blank=True, null=True, default=None)
    autogru_ck = models.BooleanField(blank=True, null=True, default=None)
    gru_autocarro = models.DateField(blank=True, null=True, default=None)
    gru_autocarro_ck = models.BooleanField(blank=True, null=True, default=None)
    carrello = models.DateField(blank=True, null=True, default=None)
    carrello_ck = models.BooleanField(blank=True, null=True, default=None)
    ple = models.DateField(blank=True, null=True, default=None)
    ple_ck = models.BooleanField(blank=True, null=True, default=None)
    rls = models.DateField(blank=True, null=True, default=None)
    rls_ck = models.BooleanField(blank=True, null=True, default=None)

    class Meta:
        ordering = ['lavoratore', ]
        verbose_name = 'Formazione'
        verbose_name_plural = 'Formazione'

    def __str__(self):
        return '%s %s' % (self.lavoratore.cognome, self.lavoratore.nome)

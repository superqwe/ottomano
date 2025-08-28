from django.db import models


class Tipologia(models.Model):
    nome = models.CharField(max_length=50, blank=True, null=True)
    faldone = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ['nome', ]

        verbose_name = 'Tipologia'
        verbose_name_plural = 'Tipologie'

    def __str__(self):
        return '%s' % self.nome


class Attrezzo(models.Model):
    in_uso = models.BooleanField(default=True)
    tipologia = models.ForeignKey(Tipologia, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50, blank=True, null=True)
    modello = models.CharField(max_length=50, blank=True, null=True)
    matricola = models.CharField(max_length=20, blank=True, null=True)
    ce = models.BooleanField(default=False)
    manuale = models.BooleanField(default=False)

    def nome(self):
        if self.matricola:
            _nome = '%s - %s - %s' % (self.marca, self.modello, self.matricola)
        else:
            _nome = '%s - %s' % (self.marca, self.modello)

        _nome = _nome.replace('/', '_').replace('.', '_')
        return _nome

    class Meta:
        ordering = ['tipologia', 'marca', 'modello', 'matricola']
        verbose_name = 'Attrezzo'
        verbose_name_plural = 'Attrezzi'

    def __str__(self):
        return self.nome()

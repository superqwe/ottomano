from django.db import models

# Create your models here.

class Lavoratore(models.Model):
    cognome = models.CharField(max_length=20)
    nome = models.CharField(max_length=20)

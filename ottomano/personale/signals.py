from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lavoratore, Formazione, Idoneita

@receiver(post_save, sender=Lavoratore)
def crea_formazione_idoneita(sender, instance, created, **kwargs):
    if created:
        Formazione.objects.create(lavoratore=instance)
        Idoneita.objects.create(lavoratore=instance)
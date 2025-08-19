from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lavoratore, Formazione, Idoneita
from icecream import ic
from .views import PATH_DOCUMENTI
from pathlib import Path


@receiver(post_save, sender=Lavoratore)
def crea_formazione_idoneita(sender, instance, created, **kwargs):
    if created:
        Formazione.objects.create(lavoratore=instance)
        Idoneita.objects.create(lavoratore=instance)

        cartella_lavoratore = Path(PATH_DOCUMENTI) / f'{instance.cognome.upper()} {instance.nome}'
        cartelle = (cartella_lavoratore,
                    cartella_lavoratore / 'attestati',
                    cartella_lavoratore / 'nomine',
                    cartella_lavoratore / 'superati',
                    cartella_lavoratore / 'vari',
                    )
        for cartella in cartelle:
            cartella.mkdir(parents=True, exist_ok=True)

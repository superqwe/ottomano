from pathlib import Path

from django.db.models.signals import post_save
from django.dispatch import receiver
from icecream import ic

from .models import Mezzo
from .views import PATH_DOCUMENTI


@receiver(post_save, sender=Mezzo)
def crea_nuovo_mezzo(sender, instance, created, **kwargs):
    if created:
        cartella_mezzo = Path(PATH_DOCUMENTI) / f'{instance}'
        cartella_mezzo.mkdir(parents=True, exist_ok=True)

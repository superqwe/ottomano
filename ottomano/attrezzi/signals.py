from pathlib import Path

from django.db.models.signals import post_save
from django.dispatch import receiver
from icecream import ic

from .models import Attrezzo
from .views import PATH_DOCUMENTI


@receiver(post_save, sender=Attrezzo)
def crea_cartella(sender, instance, created, **kwargs):
    if created:
        cartella_attrezzo = Path(PATH_DOCUMENTI) / f'{instance.tipologia}' / f'{instance}'
        cartella_attrezzo.mkdir(parents=True, exist_ok=True)

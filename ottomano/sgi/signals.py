from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import DPI_Anticaduta2

@receiver(m2m_changed, sender=DPI_Anticaduta2.operazione.through)
def aggiorna_dpi_anticaduta(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        # Ricalcola i campi in base alle operazioni
        for operazione in instance.operazione.all():
            instance.consegna2 = operazione.data

            match operazione.operazione:
                case 'ms':
                    instance.messa_in_servizio = operazione.data
                    instance.lavoratore = operazione.lavoratore
                    instance.stato = 'c'
                case 'c':
                    instance.lavoratore = operazione.lavoratore
                    instance.stato = 'c'
                case 'd':
                    instance.lavoratore = None
                    instance.stato = 'd'
                case 'rv':
                    instance.lavoratore = operazione.lavoratore
                    instance.stato = 'v'
                case 'vi':
                    instance.stato = 'vi'
                case 'v':
                    instance.data_verifica = operazione.data
                    instance.stato = 'vd'
                case 'x':
                    instance.dismissione = operazione.data
                    instance.lavoratore = operazione.lavoratore
                    instance.stato = 'x'

        if not instance.operazione.all():
            instance.lavoratore = None
            instance.stato = 'd'

        instance.save()

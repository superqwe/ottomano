# Generated by Django 4.0.2 on 2022-02-22 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personale', '0006_alter_lavoratore_cap_alter_lavoratore_provincia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lavoratore',
            name='reparto',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
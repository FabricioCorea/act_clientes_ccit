# Generated by Django 5.1.6 on 2025-05-01 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0021_historialestadosinmovimiento_genera_movimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='contacto_cargo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

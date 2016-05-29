# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0003_analisis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analisis',
            name='unidad',
        ),
        migrations.AddField(
            model_name='analisis',
            name='unidades',
            field=models.CharField(default=b'', max_length=100, blank=b'true'),
        ),
        migrations.AlterField(
            model_name='analisis',
            name='lct',
            field=models.DecimalField(null=b'true', max_digits=10, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='analisis',
            name='muestra',
            field=models.ForeignKey(to='presupuestos.Muestra'),
        ),
        migrations.AlterField(
            model_name='analisis',
            name='observacion',
            field=models.CharField(default=b'', max_length=100, blank=b'true'),
        ),
        migrations.AlterField(
            model_name='analisis',
            name='valor',
            field=models.CharField(default=b'', max_length=100, verbose_name=b'resultado', blank=b'true'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0005_auto_20160208_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muestra',
            name='referencia_clave',
            field=models.CharField(default=b'ID16-', max_length=100, blank=b'true'),
        ),
        migrations.AlterField(
            model_name='presupuesto',
            name='referencia_clave',
            field=models.CharField(default=b'SP16-', max_length=100, blank=b'true'),
        ),
        migrations.AlterUniqueTogether(
            name='matriztecnicalct',
            unique_together=set([('matriz', 'parametro', 'tecnica')]),
        ),
    ]

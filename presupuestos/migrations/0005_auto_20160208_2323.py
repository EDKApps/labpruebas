# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0004_auto_20160208_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='ot_item',
            name='muestreo_propio',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ot_item',
            name='nota_muestreo',
            field=models.CharField(max_length=200, blank=b'true'),
        ),
    ]

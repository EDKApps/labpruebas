# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0006_auto_20160529_1738'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'permissions': (('ver_cliente', 'Acceso a Clientes'),)},
        ),
    ]

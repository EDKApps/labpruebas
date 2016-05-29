# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0002_auto_20160119_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analisis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lct', models.DecimalField(max_digits=10, decimal_places=6)),
                ('valor', models.CharField(max_length=100, verbose_name=b'resultado', blank=b'true')),
                ('verificacion', models.BooleanField(default=False)),
                ('observacion', models.CharField(max_length=100, blank=b'true')),
                ('muestra', models.ForeignKey(to='presupuestos.Muestra', on_delete=django.db.models.deletion.PROTECT)),
                ('parametro', models.ForeignKey(to='presupuestos.Parametro', on_delete=django.db.models.deletion.PROTECT)),
                ('tecnica', models.ForeignKey(to='presupuestos.Tecnica', on_delete=django.db.models.deletion.PROTECT)),
                ('unidad', models.ForeignKey(to='presupuestos.Unidades', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]

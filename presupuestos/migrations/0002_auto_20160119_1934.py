# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('presupuestos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Muestra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('referencia_clave', models.CharField(default=b'M-', max_length=100, blank=b'true')),
                ('referencia', models.CharField(max_length=20, blank=b'true')),
                ('ingreso_muestra', models.CharField(max_length=100, verbose_name=b'responsable ingreso de muestra', blank=b'true')),
                ('fecha_ingreso', models.DateField(default=datetime.date.today, verbose_name=b'fecha de ingreso al sistema')),
                ('cadena_custodia', models.CharField(max_length=100, verbose_name=b'cadena de custodia', blank=b'true')),
                ('rotulo', models.CharField(max_length=100, blank=b'true')),
                ('ubicacion', models.CharField(max_length=100, verbose_name=b'ubicaci\xc3\xb3n', blank=b'true')),
                ('sitio_muestreo', models.CharField(max_length=100, verbose_name=b'sitio de muestreo', blank=b'true')),
                ('muestreador', models.CharField(max_length=100, blank=b'true')),
                ('peso', models.CharField(max_length=100, verbose_name=b's\xc3\xb3lido - peso de muestra (gr.)', blank=b'true')),
                ('volumen', models.CharField(max_length=100, verbose_name=b'l\xc3\xadquido - Vol\xc3\xbamen de muestra (lt.)', blank=b'true')),
                ('caudal', models.CharField(max_length=100, verbose_name=b'aire - Caudal, (lt/min, tiempo)', blank=b'true')),
                ('preservacion', models.CharField(max_length=100, verbose_name=b'Preservaci\xc3\xb3n - Conservaci\xc3\xb3n', blank=b'true')),
                ('fecha_muestreo', models.DateField(default=datetime.date.today, verbose_name=b'fecha de muestro')),
                ('coordenada', models.CharField(max_length=100, verbose_name=b'coordenadas de ubicaci\xc3\xb3n', blank=b'true')),
                ('sistema_coordenada', models.CharField(max_length=100, verbose_name=b'sistema de coordenada', blank=b'true')),
                ('observacion', models.CharField(max_length=100, verbose_name=b'observaci\xc3\xb3n', blank=b'true')),
            ],
        ),
        migrations.CreateModel(
            name='Muestra_Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado_actual', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='matriz',
            field=models.ForeignKey(to='presupuestos.Matriz', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='item',
            name='presupuesto',
            field=models.ForeignKey(to='presupuestos.Presupuesto', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='ot_item',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='presupuestos.Item', null=True),
        ),
        migrations.AlterField(
            model_name='subitem_parametro',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='presupuestos.Item', null=True),
        ),
        migrations.AlterField(
            model_name='subitem_parametro',
            name='itemparametro',
            field=models.ForeignKey(to='presupuestos.ParametroPrecio', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AlterField(
            model_name='subitem_perfil',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='presupuestos.Item', null=True),
        ),
        migrations.AlterField(
            model_name='subitem_perfil',
            name='itemperfil',
            field=models.ForeignKey(to='presupuestos.PerfilPrecio', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='muestra',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, default=1, to='presupuestos.Muestra_Estado'),
        ),
        migrations.AddField(
            model_name='muestra',
            name='ot_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='presupuestos.Ot_Item', null=True),
        ),
    ]

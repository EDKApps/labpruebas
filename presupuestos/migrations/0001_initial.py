# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campania',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(default=0)),
                ('descripcion', models.CharField(max_length=100)),
                ('cantidad', models.IntegerField(default=0)),
                ('unidad_medida', models.CharField(max_length=100, blank=b'true')),
                ('valor_unitario', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=5, blank=b'true', null=b'true', verbose_name=b'descuento (%)')),
                ('valor_total_sin_descuento', models.DecimalField(default=0, null=b'true', max_digits=8, decimal_places=2, blank=b'true')),
                ('valor_total_con_descuento', models.DecimalField(default=0, null=b'true', max_digits=8, decimal_places=2, blank=b'true')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('empresa', models.CharField(max_length=100)),
                ('contacto', models.CharField(max_length=200, verbose_name=b'Contacto (apellido, nombre)')),
                ('funcion', models.CharField(max_length=100, blank=b'true')),
                ('domicilio', models.CharField(max_length=100, blank=b'true')),
                ('localidad', models.CharField(max_length=200, blank=b'true')),
                ('telefono_fijo', models.CharField(max_length=100, blank=b'true')),
                ('telefono_movil', models.CharField(max_length=100, blank=b'true')),
                ('email', models.CharField(max_length=100, blank=b'true')),
                ('cuit', models.CharField(max_length=13, blank=b'true')),
                ('nota', models.CharField(max_length=200, blank=b'true')),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado_actual', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(default=0)),
                ('descripcion', models.CharField(max_length=100, blank=b'true')),
                ('cantidadMuestra', models.IntegerField(default=0)),
                ('descuento', models.DecimalField(default=0, verbose_name=b'descuento (%)', max_digits=5, decimal_places=2)),
                ('total_sin_descuento', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('total_con_descuento', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('seleccionado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Matriz',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_matriz', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MatrizTecnicaLct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lct', models.DecimalField(max_digits=10, decimal_places=6)),
                ('matriz', models.ForeignKey(to='presupuestos.Matriz', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='Numerador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30, blank=b'true')),
                ('ultimo_valor', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Orden_trabajo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('referencia_clave', models.CharField(default=b'OT-', max_length=100, blank=b'true')),
                ('referencia', models.CharField(max_length=20, blank=b'true')),
                ('descripcion', models.CharField(max_length=100, blank=b'true')),
                ('prioridad', models.CharField(max_length=100, blank=b'true')),
                ('fecha_creacion', models.DateField(default=datetime.date.today, verbose_name=b'fecha de creaci\xc3\xb3n')),
            ],
        ),
        migrations.CreateModel(
            name='Ot_Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado_actual', models.CharField(default=b'pendiente', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ot_Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(default=0)),
                ('cantidad', models.IntegerField(default=0)),
                ('estado', models.ForeignKey(to='presupuestos.Ot_Estado', on_delete=django.db.models.deletion.PROTECT)),
                ('item', models.ForeignKey(to='presupuestos.Item', null=True)),
                ('orden_trabajo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='presupuestos.Orden_trabajo', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_par', models.CharField(max_length=100, verbose_name=b'Parametro')),
                ('familia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=b'true', to='presupuestos.Familia', null=b'true')),
            ],
        ),
        migrations.CreateModel(
            name='ParametroPrecio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('precio_parametro', models.DecimalField(max_digits=8, decimal_places=2)),
                ('fecha_precio', models.DateField(default=datetime.date.today, verbose_name=b'Fecha del precio')),
                ('fuente_precio', models.CharField(max_length=100, verbose_name=b'Fuente del precio', blank=b'true')),
                ('seleccionado', models.BooleanField(default=False)),
                ('matriz', models.ForeignKey(to='presupuestos.Matriz', on_delete=django.db.models.deletion.PROTECT)),
                ('parametro', models.ForeignKey(to='presupuestos.Parametro', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='PerfilPrecio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.DecimalField(max_digits=8, decimal_places=2)),
                ('fecha_precio', models.DateField(verbose_name=b'Fecha del precio')),
                ('fuente_precio', models.CharField(max_length=100, verbose_name=b'Fuente del precio', blank=b'true')),
                ('seleccionado', models.BooleanField(default=False)),
                ('matriz', models.ForeignKey(to='presupuestos.Matriz', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='PerfilPrecio_Parametro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parametro', models.ForeignKey(to='presupuestos.Parametro', on_delete=django.db.models.deletion.PROTECT)),
                ('perfilPrecio', models.ForeignKey(to='presupuestos.PerfilPrecio', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='Plantillas_Impresion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('presupuesto_condiciones_comerciales', models.TextField(blank=b'true')),
                ('presupuesto_condiciones_tecnicas', models.TextField(blank=b'true')),
            ],
        ),
        migrations.CreateModel(
            name='Presupuesto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('referencia_clave', models.CharField(default=b'S-P', max_length=100, blank=b'true')),
                ('referencia', models.CharField(max_length=20, blank=b'true')),
                ('fecha_solicitud', models.DateField(default=datetime.date.today, verbose_name=b'fecha de solicitud')),
                ('fecha_vencimiento', models.DateField(null=b'true', verbose_name=b'fecha de vencimiento', blank=b'true')),
                ('fecha_envio', models.DateField(null=b'true', verbose_name=b'fecha de envio', blank=b'true')),
                ('fecha_aprobacion', models.DateField(null=b'true', verbose_name=b'fecha de aprobacion', blank=b'true')),
                ('descripcion', models.CharField(max_length=100)),
                ('observacion', models.CharField(max_length=100, blank=b'true')),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=5, blank=b'true', null=b'true', verbose_name=b'descuento global (%)')),
                ('impresion_introduccion', models.TextField(blank=b'true')),
                ('impresion_nota_muestreo', models.TextField(blank=b'true')),
                ('impresion_condiciones_comerciales', models.TextField(blank=b'true')),
                ('impresion_condiciones_tecnicas', models.TextField(blank=b'true')),
                ('cliente', models.ForeignKey(to='presupuestos.Cliente', on_delete=django.db.models.deletion.PROTECT)),
                ('estado', models.ForeignKey(to='presupuestos.Estado', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
        migrations.CreateModel(
            name='Subitem_parametro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('precio', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('item', models.ForeignKey(to='presupuestos.Item', null=True)),
                ('itemparametro', models.ForeignKey(to='presupuestos.ParametroPrecio')),
            ],
        ),
        migrations.CreateModel(
            name='Subitem_perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('precio', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('item', models.ForeignKey(to='presupuestos.Item', null=True)),
                ('itemperfil', models.ForeignKey(to='presupuestos.PerfilPrecio')),
            ],
        ),
        migrations.CreateModel(
            name='Tecnica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_tec', models.CharField(max_length=100, verbose_name=b'Tecnica')),
                ('derivacion', models.CharField(max_length=100, blank=b'true')),
                ('link', models.CharField(max_length=100, blank=b'true')),
                ('observacion', models.TextField(blank=b'true')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_tipo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Unidades',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre_unidad', models.CharField(max_length=100, verbose_name=b'Unidades')),
            ],
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='tipo',
            field=models.ForeignKey(to='presupuestos.Tipo', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='perfilprecio_parametro',
            name='tecnica',
            field=models.ForeignKey(to='presupuestos.Tecnica', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='parametroprecio',
            name='tecnica',
            field=models.ForeignKey(to='presupuestos.Tecnica', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='orden_trabajo',
            name='presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='presupuestos.Presupuesto', null=True),
        ),
        migrations.AddField(
            model_name='matriztecnicalct',
            name='parametro',
            field=models.ForeignKey(to='presupuestos.Parametro', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='matriztecnicalct',
            name='tecnica',
            field=models.ForeignKey(to='presupuestos.Tecnica', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='matriztecnicalct',
            name='unidad',
            field=models.ForeignKey(to='presupuestos.Unidades', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='item',
            name='matriz',
            field=models.ForeignKey(to='presupuestos.Matriz'),
        ),
        migrations.AddField(
            model_name='item',
            name='presupuesto',
            field=models.ForeignKey(to='presupuestos.Presupuesto'),
        ),
        migrations.AddField(
            model_name='campania',
            name='presupuesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='presupuestos.Presupuesto', null=True),
        ),
    ]

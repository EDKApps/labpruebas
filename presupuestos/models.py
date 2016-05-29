# -- coding: utf-8 --
# $ python manage.py makemigrations
# $ python manage.py migrate
# $ python manage.py createsuperuser
# $ python manage.py sqlmigrate rango 0001
# $ python manage.py runserver

from django.db import models
from datetime import date
from django.utils.encoding import python_2_unicode_compatible
#librerias para validar campo
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError

@python_2_unicode_compatible
class Numerador (models.Model):
	nombre = models.CharField(max_length=30, blank='true',unique=True)
	ultimo_valor = models.IntegerField(default=0)
	def __str__(self):
		return self.nombre



#numerador, created = Numerador.objects.update_or_create(
#        identifier=identifier, defaults={"name": name}
#)

from labutiles import sigNumero,completarConCeros #Como usa Numerador, lo importo después de que existe en model


@python_2_unicode_compatible
class Cliente (models.Model):
	empresa = models.CharField(max_length=100)
	contacto = models.CharField('Contacto (apellido, nombre)', max_length=200)
	funcion = models.CharField(max_length=100, blank='true')
	domicilio = models.CharField(max_length=100, blank='true')
	localidad = models.CharField(max_length=200, blank='true')
	telefono_fijo = models.CharField(max_length=100, blank='true')
	telefono_movil = models.CharField(max_length=100, blank='true')
	email = models.CharField(max_length=100, blank='true')
	cuit = models.CharField(max_length=13, blank='true')
	nota = models.CharField(max_length=200, blank='true')
	def __str__(self):
		return self.contacto+', '+self.empresa

	def delete(self, *args, **kwargs):
		if Presupuesto.objects.filter(cliente__pk= self.pk).exists():
			raise ValidationError('EL cliente esta relacionado al menos a un Presupuesto.')
		super(Cliente, self).delete(*args, **kwargs)

	class Meta:
		permissions = (
		("ver_cliente", "Acceso a Clientes"),
		)

@python_2_unicode_compatible
class Tipo (models.Model):
	nombre_tipo = models.CharField(max_length=100)
	def __str__(self):
		return self.nombre_tipo

@python_2_unicode_compatible
class Estado (models.Model):
	estado_actual = models.CharField(max_length=100)
	def __str__(self):
		return self.estado_actual

@python_2_unicode_compatible
class Presupuesto (models.Model):
	cliente = models.ForeignKey(Cliente, on_delete= models.PROTECT)
	referencia_clave = models.CharField(max_length=100, blank='true',default='SP16-')
	referencia = models.CharField(max_length=20,blank='true') #autoincremental
	fecha_solicitud = models.DateField('fecha de solicitud', default=date.today)
	fecha_vencimiento = models.DateField('fecha de vencimiento', blank='true', null='true')
	fecha_envio = models.DateField('fecha de envio', blank='true', null='true')
	fecha_aprobacion = models.DateField('fecha de aprobacion', blank='true', null='true')
	descripcion = models.CharField(max_length=100)
	tipo = models.ForeignKey(Tipo,on_delete= models.PROTECT)
	estado = models.ForeignKey(Estado,on_delete= models.PROTECT)
	observacion = models.CharField(max_length=100, blank='true')
	descuento = models.DecimalField('descuento global (%)', max_digits=5, decimal_places=2, null='true', blank='true', default=0)

	impresion_introduccion = models.TextField(blank='true')
	impresion_nota_muestreo = models.TextField(blank='true')
	impresion_condiciones_comerciales = models.TextField(blank='true')
	impresion_condiciones_tecnicas = models.TextField(blank='true')

	def __str__(self):
		return self.referencia

	def referencia_completa(self):
		return self.referencia_clave + self.referencia

	def total_sin_descuento(self):
		total = 0
		#Recorre los item de analis y suma el precio
		lista_items = Item.objects.filter(presupuesto = self)
		for item in lista_items:
			total = total + item.total_con_descuento

		#Recorre los item de muestreo-campania y suma el precio
		lista_items = Campania.objects.filter(presupuesto = self)
		for item in lista_items:
			total = total + item.valor_total_con_descuento
		return total

	def total_con_descuento(self):
		total_sin = self.total_sin_descuento()
		total = total_sin * (100-self.descuento) /100
		total = round (total, 2)
		return total

	def save(self, *args, **kwargs):
		#si es insert (id= 0), asignar referencia autoincremental
		if self.id is None:
			self.referencia = completarConCeros( sigNumero('presupuesto_referencia'), 5) #completo hasta 5 dígitos
		#si es insert (id= 0), asignar datos de plantilla impresion
		if self.id is None:
			plantillas = Plantillas_Impresion.objects.all()
			#una plantilla
			plantilla = plantillas[0]
			self.impresion_condiciones_comerciales = plantilla.presupuesto_condiciones_comerciales
			self.impresion_condiciones_tecnicas = plantilla.presupuesto_condiciones_tecnicas

		super(Presupuesto, self).save(*args, **kwargs) # Call the "real" save() method.

	def delete(self, *args, **kwargs):
		if Item.objects.filter(presupuesto__pk= self.pk).exists():
			raise ValidationError('EL presupuesto esta relacionado al menos a un Item.')
		super(Presupuesto, self).delete(*args, **kwargs)

@python_2_unicode_compatible
class Matriz (models.Model):
	nombre_matriz = models.CharField(max_length=100)
	def __str__(self):
		return self.nombre_matriz

	def delete(self, *args, **kwargs):
		if Item.objects.filter(matriz__pk= self.pk).exists():
			raise ValidationError('La matriz esta relacionada al menos a un Item.')
		super(Matriz, self).delete(*args, **kwargs)

@python_2_unicode_compatible
class Familia (models.Model): # también llamada Grupo
	nombre= models.CharField(max_length=100)
	def __str__(self):
		return self.nombre

	def delete(self, *args, **kwargs):
		if Parametro.objects.filter(familia__pk= self.pk).exists():
			raise ValidationError('El grupo esta relacionado al menos a un parametro.')

		super(Familia, self).delete(*args, **kwargs)

@python_2_unicode_compatible
class Parametro (models.Model):
	nombre_par = models.CharField('Parametro', max_length=100)
	familia = models.ForeignKey(Familia, blank='true', null='true', on_delete= models.PROTECT )
	def __str__(self):
		return self.nombre_par

	def delete(self, *args, **kwargs):
		if ParametroPrecio.objects.filter(parametro__pk= self.pk).exists():
			raise ValidationError('El parametro esta relacionado al menos a un Parametro Precio.')
		super(Parametro, self).delete(*args, **kwargs)


@python_2_unicode_compatible
class Tecnica (models.Model):
	nombre_tec = models.CharField('Tecnica', max_length=100)
	derivacion= models.CharField(max_length=100, blank='true')
	link = models.CharField(max_length=100, blank='true')
	observacion = models.TextField(blank='true')
	def __str__(self):
		return self.nombre_tec

	def delete(self, *args, **kwargs):
		if ParametroPrecio.objects.filter(tecnica__pk= self.pk).exists():
			raise ValidationError('La tecnica esta relacionado al menos a un Parametro Precio.')
		super(Tecnica, self).delete(*args, **kwargs)

@python_2_unicode_compatible
class Unidades (models.Model):
	nombre_unidad = models.CharField('Unidades', max_length=100)
	def __str__(self):
		return self.nombre_unidad

	def delete(self, *args, **kwargs):
		if MatrizTecnicaLct.objects.filter(unidad__pk= self.pk).exists():
			raise ValidationError('La unidad esta relacionada al menos a un Lq.')
		super(Unidades, self).delete(*args, **kwargs)

@python_2_unicode_compatible
class MatrizTecnicaLct (models.Model):
	matriz = models.ForeignKey(Matriz, on_delete= models.PROTECT)
	parametro = models.ForeignKey(Parametro, on_delete= models.PROTECT)
	tecnica = models.ForeignKey(Tecnica, on_delete= models.PROTECT)
	lct = models.DecimalField(max_digits=10, decimal_places=6)
	unidad = models.ForeignKey(Unidades, on_delete= models.PROTECT)

	class Meta:
		unique_together = ('matriz', 'parametro', 'tecnica')

	def __str__(self):
		return self.matriz.nombre_matriz+', '+self.parametro.nombre_par+', '+self.tecnica.nombre_tec

@python_2_unicode_compatible
class ParametroPrecio  (models.Model):
	matriz = models.ForeignKey(Matriz, on_delete= models.PROTECT)
	parametro = models.ForeignKey(Parametro, on_delete= models.PROTECT)
	tecnica = models.ForeignKey(Tecnica, on_delete= models.PROTECT)
	precio_parametro = models.DecimalField(max_digits=8, decimal_places=2)
	fecha_precio = models.DateField('Fecha del precio', default=date.today)
	fuente_precio = models.CharField('Fuente del precio', max_length=100, blank='true')
	seleccionado = models.BooleanField(default=False)
	#def familia(self): todo: (Inferido) a partir del parametro retornar su familia

	def lct(self):
		try:
			mt = MatrizTecnicaLct.objects.get(matriz=self.matriz, parametro=self.parametro, tecnica=self.tecnica)
		except MatrizTecnicaLct.DoesNotExist:
			return 0
		else:
			return mt.lct
	def unidades(self):
		try:
			mt = MatrizTecnicaLct.objects.get(matriz=self.matriz, parametro=self.parametro, tecnica=self.tecnica)
		except MatrizTecnicaLct.DoesNotExist:
			return ''
		else:
			#devuelve el string, y no el objeto
			return mt.unidad.nombre_unidad
	def __str__(self):
		return self.parametro.nombre_par+', '+self.tecnica.nombre_tec

	def delete(self, *args, **kwargs):
		if Subitem_parametro.objects.filter(itemparametro__pk= self.pk).exists():
			raise ValidationError('El precio esta relacionado a un Item')
		super(ParametroPrecio, self).delete(*args, **kwargs)

@python_2_unicode_compatible
class PerfilPrecio (models.Model): # ex GrupoParametroPrecio
	nombre = models.CharField( max_length=100)
	matriz = models.ForeignKey(Matriz, on_delete= models.PROTECT)
	precio = models.DecimalField(max_digits=8, decimal_places=2)
	fecha_precio = models.DateField('Fecha del precio')
	fuente_precio = models.CharField('Fuente del precio', max_length=100, blank='true')
	seleccionado = models.BooleanField(default=False)
	def __str__(self):
		return self.nombre

	def delete(self, *args, **kwargs):
		if PerfilPrecio_Parametro.objects.filter(perfilPrecio__pk= self.pk).exists():
			raise ValidationError('El precio esta relacionado a un parametro del perfil')
		super(PerfilPrecio, self).delete(*args, **kwargs)

@python_2_unicode_compatible
class PerfilPrecio_Parametro (models.Model): # ex GrupoParametroPrecio_Parametro
	perfilPrecio = models.ForeignKey(PerfilPrecio, on_delete= models.PROTECT)
	parametro = models.ForeignKey(Parametro, on_delete= models.PROTECT)
	tecnica = models.ForeignKey(Tecnica, on_delete= models.PROTECT)

	def lct(self):
		try:
			mt = MatrizTecnicaLct.objects.get(matriz=self.perfilPrecio.matriz, parametro=self.parametro, tecnica=self.tecnica)
		except MatrizTecnicaLct.DoesNotExist:
			return 0
		else:
			return mt.lct
	def unidades(self):
		try:
			mt = MatrizTecnicaLct.objects.get(matriz=self.perfilPrecio.matriz, parametro=self.parametro, tecnica=self.tecnica)
		except MatrizTecnicaLct.DoesNotExist:
			return ''
		else:
			#devuelve el string, y no el objeto
			return mt.unidad.nombre_unidad
	def __str__(self):
		return self.parametro.nombre_par


@python_2_unicode_compatible
class Item (models.Model): #si se elimina el presupuesto. se elimina el Item, junto con sus subitems
	presupuesto = models.ForeignKey(Presupuesto, on_delete= models.PROTECT)
	numero = models.IntegerField(default= 0)
	descripcion = models.CharField(max_length= 100, blank='true')
	matriz = models.ForeignKey(Matriz, on_delete= models.PROTECT)
	cantidadMuestra = models.IntegerField(default= 0)
	descuento = models.DecimalField('descuento (%)', max_digits=5, decimal_places=2, default=0)
	total_sin_descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	total_con_descuento = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	seleccionado = models.BooleanField(default=False)

	def __str__(self):
		return self.descripcion

	def costo_unitario(self):
		costo_unitario = self.total_sin_descuento / self.cantidadMuestra
		return costo_unitario

	def save(self, *args, **kwargs):
		#Todo - hacer no suma al eliminar un registro.
		#Pruebas para actualizar el queryset
		#objects.updates no funciono. Subitem_parametro.objects.update()
		#subitem_parametro.refresh_from_db(), no anduvo
		#Subitem_parametro.objects.refresh(), no anduvo
		#lista_subitem_parametros.refresh(), no anduvo

		#completa total
		total = 0
		#Recorre los parametros y suma el precio
		lista_subitem_parametros = Subitem_parametro.objects.filter(item = self)
		for subitem_parametro in lista_subitem_parametros:
			total = total + subitem_parametro.precio

		#Recorre los perfiles y suma el precio
		lista_subitem_perfiles = Subitem_perfil.objects.filter(item = self)
		for subitem_perfil in lista_subitem_perfiles:
			total = total + subitem_perfil.precio

		self.total_sin_descuento = total * self.cantidadMuestra
		self.total_con_descuento = self.total_sin_descuento * (100-self.descuento)/100
		# Call the "real" save() method.
		super(Item, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Subitem_parametro (models.Model): #relacion Item-ParametroPrecio
	item = models.ForeignKey(Item, null=True, on_delete= models.PROTECT)
	itemparametro = models.ForeignKey(ParametroPrecio, on_delete= models.PROTECT)
	precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	def __str__(self):
		return self.itemparametro.parametro.nombre_par #lo agrego para cumplir con decorator python_2

	def save(self, *args, **kwargs):
		#completa precio
		self.precio = self.itemparametro.precio_parametro
		# Call the "real" save() method.
		super(Subitem_parametro, self).save(*args, **kwargs)

		self.item.save()

	def delete(self, *args, **kwargs):
		item = self.item
		super(Subitem_parametro, self).delete(*args, **kwargs)
		item.save() #actualizo el item

@python_2_unicode_compatible
class Subitem_perfil (models.Model): #relacion Item-PerfilPrecio
	item = models.ForeignKey(Item, null=True, on_delete= models.PROTECT)
	itemperfil = models.ForeignKey(PerfilPrecio, on_delete= models.PROTECT)
	precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	def __str__(self):
		return self.itemperfil.nombre #lo agrego para cumplir con decorator python_2

	def save(self, *args, **kwargs):
		#completa precio
		self.precio = self.itemperfil.precio
		# Call the "real" save() method.
		super(Subitem_perfil, self).save(*args, **kwargs)
		self.item.save()

	def delete(self, *args, **kwargs):
		item = self.item
		super(Subitem_perfil, self).delete(*args, **kwargs)
		item.save() #actualizo el item

@python_2_unicode_compatible
class Campania (models.Model):
	presupuesto = models.ForeignKey(Presupuesto, on_delete= models.PROTECT, null=True)
	numero = models.IntegerField(default= 0)
	descripcion = models.CharField(max_length= 100)
	cantidad = models.IntegerField(default= 0)
	unidad_medida = models.CharField(max_length= 100, blank='true')
	valor_unitario = models.DecimalField(max_digits=8, decimal_places=2, default= 0)
	descuento = models.DecimalField('descuento (%)', max_digits=5, decimal_places=2, null='true', blank='true', default=0)
	valor_total_sin_descuento = models.DecimalField(max_digits=8, decimal_places=2, null='true', blank='true', default=0)
	valor_total_con_descuento = models.DecimalField(max_digits=8, decimal_places=2, null='true', blank='true', default=0)
	def __str__(self):
		return self.descripcion

	def save(self, *args, **kwargs):
		#completa valor_total
		self.valor_total_sin_descuento = self.valor_unitario * self.cantidad
		self.valor_total_con_descuento = self.valor_unitario * self.cantidad * (100-self.descuento)/100

		# Call the "real" save() method.
		super(Campania, self).save(*args, **kwargs)

@python_2_unicode_compatible
class Plantillas_Impresion (models.Model):
	presupuesto_condiciones_comerciales = models.TextField(blank='true')
	presupuesto_condiciones_tecnicas = models.TextField(blank='true')
	def __str__(self):
		return 'plantillas'

@python_2_unicode_compatible
class Orden_trabajo (models.Model):
	presupuesto = models.ForeignKey(Presupuesto, on_delete= models.PROTECT, null=True)
	referencia_clave = models.CharField(max_length=100, blank='true',default='OT-')
	referencia = models.CharField(max_length=20,blank='true') #autoincremental
	descripcion = models.CharField(max_length=100, blank='true')
	prioridad = models.CharField(max_length=100, blank='true')
	fecha_creacion = models.DateField('fecha de creación', default=date.today)

	def __str__(self):
		return self.referencia

	def referencia_completa(self):
		return self.referencia_clave + self.referencia

	def save(self, *args, **kwargs):
		#si es insert (id= 0), asignar referencia autoincremental
		if self.id is None:
			self.referencia = completarConCeros( sigNumero('orden_trabajo_referencia'), 7)
		super(Orden_trabajo, self).save(*args, **kwargs) # Call the "real" save() method.

	def delete(self, *args, **kwargs):
		if Ot_Item.objects.filter(orden_trabajo__pk= self.pk).exists():
			raise ValidationError('La orden de trabajo esta relacionada al menos a un Item.')
		super(Orden_trabajo, self).delete(*args, **kwargs)


@python_2_unicode_compatible
class Ot_Estado (models.Model):
	estado_actual = models.CharField(max_length=100,default='pendiente')
	def __str__(self):
		return self.estado_actual

@python_2_unicode_compatible
class Ot_Item (models.Model):
	orden_trabajo = models.ForeignKey(Orden_trabajo, on_delete= models.PROTECT, null=True)
	item = models.ForeignKey(Item, null=True, on_delete= models.PROTECT)
	numero = models.IntegerField(default= 0)
	cantidad = models.IntegerField(default= 0)
	estado = models.ForeignKey(Ot_Estado,on_delete= models.PROTECT)
	muestreo_propio = models.BooleanField(default=False)
	nota_muestreo = models.CharField(max_length=200, blank='true')

	def __str__(self):
		return str(self.numero)

	def referencia_completa(self):
		return self.orden_trabajo.referencia_completa()+', '+str(self.numero)

	def clean(self):
		#Verifica que la (sumaCantidadItemOt < cantidad) de los item del presupuesto
		#crea una lista con las ot item de ese item-presupuesto
		lista_Ot_Item = Ot_Item.objects.filter (item = self.item)
		#suma cantidad de cada ot item
		sumaCantidadItemOt = 0

		for ot_Item in lista_Ot_Item:
			#Sí es el ot_item que se modifico, sumo cantidad
			if ((ot_Item.orden_trabajo == self.orden_trabajo) & (ot_Item.item == self.item)):
				sumaCantidadItemOt += self.cantidad
			else:
				sumaCantidadItemOt += ot_Item.cantidad
		if (sumaCantidadItemOt>self.item.cantidadMuestra):
			raise ValidationError({'cantidad':_('Error: cantidad debe ser menor que presupuesto.item.cantidad. Verifique si existen otras OT con este presupuesto')})

@python_2_unicode_compatible
class Muestra_Estado (models.Model):
	estado_actual = models.CharField(max_length=100)
	def __str__(self):
		return self.estado_actual

@python_2_unicode_compatible
class Muestra (models.Model):
	ot_item = models.ForeignKey(Ot_Item, null=True, on_delete= models.PROTECT)
	referencia_clave = models.CharField(max_length=100, blank='true',default='ID16-')
	referencia = models.CharField(max_length=20,blank='true') #autoincremental, ajustado en save()
	ingreso_muestra = models.CharField('responsable ingreso de muestra', max_length=100, blank='true')
	fecha_ingreso = models.DateField('fecha de ingreso al sistema', default=date.today)
	cadena_custodia = models.CharField('cadena de custodia', max_length=100, blank='true')
	rotulo = models.CharField(max_length=100, blank='true')
	ubicacion = models.CharField('ubicación', max_length=100, blank='true')
	sitio_muestreo = models.CharField('sitio de muestreo', max_length=100, blank='true')
	muestreador = models.CharField(max_length=100, blank='true')
	peso = models.CharField('sólido - peso de muestra (gr.)', max_length=100, blank='true')
	volumen = models.CharField('líquido - Volúmen de muestra (lt.)', max_length=100, blank='true')
	caudal = models.CharField('aire - Caudal, (lt/min, tiempo)', max_length=100, blank='true')
	preservacion = models.CharField('Preservación - Conservación', max_length=100, blank='true')
	fecha_muestreo = models.DateField('fecha de muestro', default=date.today)
	coordenada = models.CharField('coordenadas de ubicación', max_length=100, blank='true')
	sistema_coordenada = models.CharField('sistema de coordenada', max_length=100, blank='true')
	observacion = models.CharField('observación', max_length=100, blank='true')
	estado = models.ForeignKey(Muestra_Estado,on_delete= models.PROTECT, default=1)

	def __str__(self):
		return self.referencia

	def referencia_completa(self):
		return self.referencia_clave + self.referencia

	def save(self, *args, **kwargs):
		#si es insert (id= 0), asignar referencia autoincremental
		if self.id is None:
			self.referencia = completarConCeros( sigNumero('muestra_referencia'), 7) #completo hasta 7 dígitos

		#Si es nueva muestra, crea los registro de Analisis
		if not(Muestra.objects.filter(id=self.id).exists()):
			crear_analisis =  True
		else:
			crear_analisis = False

		# Call the "real" save() method.
		super(Muestra, self).save(*args, **kwargs)

		if crear_analisis:
			#Buscar OtItem - Item - sus Subitem_parametro --sus parametros
			lista_subitem_parametro = Subitem_parametro.objects.filter (item = self.ot_item.item)
			for subitem_parametro in lista_subitem_parametro:
				un_analisis = Analisis.objects.create(muestra=self, parametro=subitem_parametro.itemparametro.parametro, tecnica=subitem_parametro.itemparametro.tecnica, unidades = subitem_parametro.itemparametro.unidades(), lct =  subitem_parametro.itemparametro.lct())
				un_analisis.save()
			#Buscar OtItem - Item - sus perfilPrecio - sus parametros
			lista_Subitem_perfil = Subitem_perfil.objects.filter (item = self.ot_item.item)
			for un_subitem_perfil in lista_Subitem_perfil:
				#todo hacer, no funciona
				#Verificar linea, instance
				lista_perfilPrecio_par = PerfilPrecio_Parametro.objects.filter(perfilPrecio=un_subitem_perfil.itemperfil)
				for perfilPrecio_Par in lista_perfilPrecio_par:
					un_analisis = Analisis.objects.create(muestra=self, parametro=perfilPrecio_Par.parametro, tecnica=perfilPrecio_Par.tecnica, unidades = perfilPrecio_Par.unidades(), lct =  perfilPrecio_Par.lct())
					un_analisis.save()


	def clean(self):
		#validar que fecha muestreo < fecha ingreso
		if (self.fecha_muestreo > self.fecha_ingreso):
			raise ValidationError({'fecha_muestreo':_('Error: fecha muestreo debe ser menor que fecha ingreso.')})
		#validar que el numero de muestra < que otitem.cantidad
		numero_muestras = Muestra.objects.filter (ot_item = self.ot_item).count()
		if not(Muestra.objects.filter(id=self.id).exists()):
			if ((numero_muestras+1) > self.ot_item.cantidad):
				raise ValidationError({'referencia_clave':_('Error: numero de muestras debe ser menor qu ot-item.cantidad .')})

@python_2_unicode_compatible
class Analisis (models.Model):
	#Si se elimina la muestra, se borran los analisis también
	muestra = models.ForeignKey(Muestra)
	parametro = models.ForeignKey(Parametro, on_delete= models.PROTECT)
	tecnica = models.ForeignKey(Tecnica, on_delete= models.PROTECT)
	#Se optó que sea Charfield, y no foreingkey para simplificar.
	unidades = models.CharField(max_length=100, blank='true', default='')
	lct = models.DecimalField(max_digits=10, decimal_places=6, null='true')
	valor = models.CharField('resultado', max_length=100, blank='true', default='')
	verificacion = models.BooleanField(default=False)
	observacion = models.CharField(max_length=100, blank='true', default='')

	def __str__(self):
		return self.muestra.referencia+', '+self.parametro.nombre_par

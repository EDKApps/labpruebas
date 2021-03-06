#!/usr/bin/env python 
#-- coding: utf-8 --
#from django.db import models
from .models import Orden_trabajo, Presupuesto, Ot_Item, Item, Muestra, Analisis

def protocoloimpresion(idot):
	ot = Orden_trabajo.objects.get(id=idot)
	plantilla = '<h2 class="EDKAppsTituloCentrado" >Protocolo</h2>'
	plantilla += '<p>Orden de trabajo: {0}</p>'.format(ot.referencia_completa())
	plantilla += '<p>Descripción: {0}</p>'.format(ot.descripcion.encode('utf-8'))
	plantilla += '<p>Cliente: {0}</p>'.format(ot.presupuesto.cliente)
	plantilla += '<p>Domicilio: {0}</p>'.format(ot.presupuesto.cliente.domicilio.encode('utf-8'))
	plantilla += '<p>Localidad: {0}</p>'.format(ot.presupuesto.cliente.localidad.encode('utf-8'))
	plantilla += '<p>Telefono fijo/movil: {0}, {1}</p>'.format(ot.presupuesto.cliente.telefono_fijo,ot.presupuesto.cliente.telefono_movil)
	plantilla += '<p>Email: {0}</p>'.format(ot.presupuesto.cliente.email.encode('utf-8'))
	plantilla += '<h2 class="EDKAppsTituloCentrado" >Presupuesto {0}</h2>'.format(ot.presupuesto)
	plantilla += '<p>Descripción: {0}</p>'.format(ot.presupuesto.descripcion.encode('utf-8'))
	plantilla += '<p>Fecha de creación: {0}</p>'.format(ot.fecha_creacion)
	plantilla += '<br/>'
	plantilla += '<b>Detalles de items </b>'
	mensajeSinMuestreoPropio=True
	for otitem in Ot_Item.objects.filter(orden_trabajo=ot).order_by('numero'):
		#Verifica muestreo propio
		if (otitem.muestreo_propio==True):
			mensajeSinMuestreoPropio=False
		plantilla += '<p>______</p>'
		plantilla += '<b>Item: {0}</b>'.format(otitem.numero)
		plantilla += '<p>Descipción: {0}</p>'.format(otitem.item)
		plantilla += '<p>Cantidad: {0}</p>'.format(otitem.cantidad)
		plantilla += '<p>Estado {0}</p>'.format(otitem.estado)
		for muestra in Muestra.objects.filter(ot_item=otitem).order_by('referencia'):
			if (muestra.estado.estado_actual=='analizada'):
				plantilla += '<p class="EDKAppsLineaHorizontal" ></p>'
				plantilla += '<b>Muestra: {0}</b>'.format(muestra.referencia_completa())
				plantilla += '<p>Ingreso de la muestra: {0}</p>'.format(muestra.ingreso_muestra.encode('utf-8'))
				plantilla += '<p>Fecha de ingreso: {0}</p>'.format(muestra.fecha_ingreso)
				plantilla += '<p>Cadena de custodia: {0}</p>'.format(muestra.cadena_custodia.encode('utf-8'))
				plantilla += '<p>Rotulo: {0}</p>'.format(muestra.rotulo)
				plantilla += '<p>Ubicación: {0}</p>'.format(muestra.ubicacion.encode('utf-8'))
				plantilla += '<p>Sitio: {0}</p>'.format(muestra.sitio_muestreo.encode('utf-8'))
				plantilla += '<p>Muestreador: {0}</p>'.format(muestra.muestreador.encode('utf-8'))
				if not muestra.peso:
					plantilla += ''
				else:
					plantilla += '<p>Peso: {0}</p>'.format(muestra.peso.encode('utf-8'))
				if not muestra.volumen:
					plantilla += ''
				else:
					plantilla += '<p>Volumen: {0}</p>'.format(muestra.volumen.encode('utf-8'))
				if not muestra.caudal:
					plantilla += ''
				else:
					plantilla += '<p>Caudal: {0}</p>'.format(muestra.caudal.encode('utf-8'))
				plantilla += '<p>Preservación: {0}</p>'.format(muestra.preservacion.encode('utf-8'))
				plantilla += '<p>Fecha Muestreo: {0}</p>'.format(muestra.fecha_muestreo)
				plantilla += '<p>Coordenadas: {0}</p>'.format(muestra.coordenada.encode('utf-8'))
				plantilla += '<p>Sistema de las coordenadas: {0}</p>'.format(muestra.sistema_coordenada.encode('utf-8'))
				plantilla += '<p>Observación: {0}</p>'.format(muestra.observacion.encode('utf-8'))
				plantilla += '<br/>'
				plantilla += '<b>Analisis resumen</b>'
				plantilla += '<table>'
				plantilla += '<tr>'
				plantilla += '<td>Parametro </td>'
				plantilla += '<td> Técnica </td>'
				plantilla += '<td>Unidad </td>'
				plantilla += '<td>LCT </td>'
				plantilla += '<td>Resultado </td>'
				plantilla += '</tr>'
				for analisis in Analisis.objects.filter(muestra=muestra).order_by('parametro__nombre_par'):
					plantilla += '<tr>'
					plantilla += '<td>{0}</td>'.format(analisis.parametro)
					plantilla += '<td>{0}</td>'.format(analisis.tecnica)
					plantilla += '<td>{0}</td>'.format(analisis.unidades.encode('utf-8'))
					plantilla += '<td>{0}</td>'.format(analisis.lct)
					plantilla += '<td>{0}</td>'.format(analisis.valor.encode('utf-8'))
					plantilla += '</tr>'
				plantilla += '</table>'
				plantilla += '<br/>'
				plantilla += '<b>Analisis con verificación</b>'
				cont = 1
				plantilla += '<table>' 
				for analisis in Analisis.objects.filter(muestra=muestra, verificacion=True).order_by('parametro__nombre_par'):
					if (cont<=1):
						plantilla += '<tr>'
						plantilla += '<td>Parametro </td>'
						plantilla += '<td> Técnica </td>'
						plantilla += '<td>Unidad </td>'
						plantilla += '<td>LCT</td>'
						plantilla += '<td>Resultado </td>'
						plantilla += '<td>Verificación </td>'
						plantilla += '<td>Observación </td>'
						plantilla += '</tr>'
						cont += 1
					plantilla += '<tr>'
					plantilla += '<td>{0}</td>'.format(analisis.parametro)
					plantilla += '<td>{0}</td>'.format(analisis.tecnica)
					plantilla += '<td>{0}</td>'.format(analisis.unidades.encode('utf-8'))
					plantilla += '<td>{0}</td>'.format(analisis.lct)
					plantilla += '<td>{0}</td>'.format(analisis.valor.encode('utf-8'))
					plantilla += '<td>Verificado</td>'
					plantilla += '<td>{0}</td>'.format(analisis.observacion.encode('utf-8'))
					plantilla += '</tr>'
				plantilla += '</table>' 
				if (cont==1):
					plantilla += '<p>No existe ningun item vereficado en la muestra</p>'
				else:
					plantilla += '<p></p>'
					
				if (mensajeSinMuestreoPropio==True):
					plantilla += '<br/>'
					plantilla += '<p>La toma de muestras no ha sido ejecutada por personal de nuestro Laboratorio.</p>'
				else:
					plantilla += '<p></p>'
					
			else:
				plantilla += '<p></p>'
												
	return plantilla

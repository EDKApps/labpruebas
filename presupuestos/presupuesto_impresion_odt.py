#!/usr/bin/env python 
#-- coding: utf-8 --
#from django.db import models
from datetime import datetime, date, time, timedelta
from .models import Presupuesto, Item, Subitem_perfil, Campania, Subitem_parametro, PerfilPrecio_Parametro

#Presupuesto

def impresion(idpresupuesto):
    presupuesto = Presupuesto.objects.get(id=idpresupuesto)
    cadena_html = '<p class="EDKAppsTituloCentrado">Presupuesto</p>'
    hora = datetime.today()
    cadena_html += '<p class="EDKAppsDerecho">Fecha: {0}</p>'.format(hora.strftime('%d/%m/%Y'))
    cadena_html += '<p>Presupuesto número: {0}</p>'.format(presupuesto.referencia_completa())
    cadena_html += '<b>Datos del Cliente</b>'
    cadena_html += '<p>Cliente: {0}</p>'.format(presupuesto.cliente.empresa.encode('utf-8'))
    cadena_html += '<p>Cuit: {0}</p>'.format(presupuesto.cliente.cuit)
    cadena_html += '<p>Contacto: {0}</p>'.format(presupuesto.cliente.contacto.encode('utf-8'))
    cadena_html += '<p>Domicilio: {0}</p>'.format(presupuesto.cliente.domicilio.encode('utf-8'))
    cadena_html += '<p>Telefono: {0}, {1}</p>'.format(presupuesto.cliente.telefono_fijo, presupuesto.cliente.telefono_movil)
    cadena_html += '<p>Email: {0}</p>'.format(presupuesto.cliente.email)
    
    cadena_html += '<b>Datos del Presupuesto</b>'
    cadena_html += '<p>Introducción: {0}</p>'.format(presupuesto.impresion_introduccion.encode('utf-8'))
    cadena_html += '<p>Descripcion: {0}</p>'.format(presupuesto.descripcion.encode('utf-8'))
    cadena_html += '<p>Tipo: {0}</p>'.format(presupuesto.tipo)
    cadena_html += '<p></p>'
    #cadena_html += '<p>Descuento (%): {0}</p>'.format(presupuesto.descuento)
    cadena_html += '<p class="EDKAppsLineaHorizontal" ></p>'

    cadena_html += '<b>Detalle de Item</b>'
    for item in Item.objects.filter(presupuesto=presupuesto).order_by("numero"):
        cadena_html += '<p><b>Item {0}</b></p>'.format(item.numero)
        cadena_html += '<p>Matriz: {0}</p>'.format(item.matriz)
        cadena_html += '<p>Descripcion: {0}</p>'.format(item.descripcion.encode('utf-8'))
        cadena_html += '<p>Cantidad de muestras: {0}</p>'.format(item.cantidadMuestra)
        cadena_html += '<p>Costo Unitario: {0}</p>'.format(item.costo_unitario())
        cadena_html += '<p>Descuento: {0}</p>'.format(item.descuento)
        cadena_html += '<p>Total sin descuento: {0}</p>'.format(item.total_sin_descuento)	
        cadena_html += '<p>Total con descuento: {0}</p>'.format(item.total_con_descuento)
        cadena_html +=  '<br/>'

        cadena_html += '<table>'
        cadena_html += '<tr>'
        cadena_html += '<td>Perfil</td>'
        cadena_html += '<td>Parametro</td>'
        cadena_html += '<td>Metodologia analitica</td>'
        cadena_html += '<td>Costo unitario, Por muestra</td>'
        cadena_html += '</tr>'
        lista = Subitem_parametro.objects.filter(item = item)
        for subitem_parametro in lista:
            cadena_html += '<tr>'
            cadena_html += '<td>--</td>'
            cadena_html += '<td>{0}</td>'.format(subitem_parametro.itemparametro.parametro)
            cadena_html += '<td>{0}</td>'.format(subitem_parametro.itemparametro.tecnica)
            cadena_html += '<td>{0}</td>'.format(subitem_parametro.precio)
            cadena_html += '</tr>'
        if not lista:
            cadena_html += '<tr>'
            cadena_html += '<td></td>'
            cadena_html += '<td>No hay parametros registrados</td>'
            cadena_html += '<td></td>'
            cadena_html += '<td></td>'
            cadena_html += '</tr>'
        for subitem_perfil in Subitem_perfil.objects.filter(item=item):
            cadena_html += '<tr>'
            cadena_html += '<td>{0}</td>'.format(subitem_perfil.itemperfil.nombre.encode('utf-8'))
            cadena_html += '<td></td>'
            cadena_html += '<td></td>'
            cadena_html += '<td>{0}</td>'.format(subitem_perfil.precio)
            cadena_html += '</tr>'
            for perfilPrecio_Par in PerfilPrecio_Parametro.objects.filter(perfilPrecio = subitem_perfil.itemperfil):	
                cadena_html += '<tr>'
                cadena_html += '<td></td>'
                cadena_html += '<td>{0}</td>'.format(perfilPrecio_Par.parametro)
                cadena_html += '<td>{0}</td>'.format(perfilPrecio_Par.tecnica)
                cadena_html += '<td>--</td>'
                cadena_html += '<td></td>'
                cadena_html += '</tr>'
        cadena_html += '</table>'
        cadena_html += '<br/>'


    listaMuestreo = Campania.objects.filter(presupuesto=presupuesto).order_by("numero")
    if (listaMuestreo):
        cadena_html += '<h2>Muestreo: </h2>'
        cadena_html += '<table>'
        cadena_html += '<tr>'
        cadena_html += '<td>Numero</td>'
        cadena_html += '<td>Descripcion</td>'
        cadena_html += '<td>Cantidad</td>'
        cadena_html += '<td>Unidad de medida</td>'
        cadena_html += '<td>Valor unitario</td>'
        cadena_html += '<td>Descuento</td>'
        cadena_html += '<td>Valor total</td>'
        cadena_html += '</tr>'
        for campania in listaMuestreo:
            cadena_html += '<tr>'
            cadena_html += '<td>{0}</td>'.format(campania.numero)
            cadena_html += '<td>{0}</td>'.format(campania.descripcion.encode('utf-8'))
            cadena_html += '<td>{0}</td>'.format(campania.cantidad)
            cadena_html += '<td>{0}</td>'.format(campania.unidad_medida.encode('utf-8'))
            cadena_html += '<td>{0}</td>'.format(campania.valor_unitario)
            cadena_html += '<td>{0}</td>'.format(campania.descuento)
            cadena_html += '<td>{0}</td>'.format(campania.valor_total_con_descuento)
            cadena_html += '</tr>'
        cadena_html += '</table>'
        cadena_html += '<br/>'
        cadena_html += '<p>Nota: {0}</p>'.format(presupuesto.impresion_nota_muestreo.encode('utf-8'))


    cadena_html += '<h2>Resumen del presupuesto</h2>'
    cadena_html += '<p><b>Total General</b></p>'
    cadena_html += '<p>Presupuesto numero: {0}</p>'.format(presupuesto.referencia_completa())
    cadena_html += '<p>Total: {0}</p>'.format(presupuesto.total_sin_descuento())
    if (presupuesto.descuento!=0):
        cadena_html += '<p>Descuento: {0}%</p>'.format(presupuesto.descuento) 
        cadena_html += '<p>Total con descuento: {0}</p>'.format(presupuesto.total_con_descuento())

    cadena_html += '<p class="EDKAppsLineaHorizontal" ></p>'
    cadena_html += '<p><b>Condiciones Generales y notas técnicas</b></p>'
    cadena_html += '<br/>' 
    #cadena_html += '<p class="EDKAppsJustificado">Condiciones comerciales
    cadena_html += '<p>Condiciones comerciales: {0}</p>'.format(presupuesto.impresion_condiciones_comerciales.encode('utf-8'))
    cadena_html += '<br/>'
    cadena_html += '<p>Notas técnicas: {0}</p>'.format(presupuesto.impresion_condiciones_tecnicas.encode('utf-8'))

    cadena_html_ajuste = cadena_html.replace('\n','<br/>')
    
    return cadena_html_ajuste


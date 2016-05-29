# -*- encoding: utf-8 -*-
"""
utilidades para usar desde distintos puntos del sistema
"""
from .models import Numerador

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#path a plantillas odt. Ejemplo: /opt/EDKAppsLab/labpg/plantillas_odt
PLANTILLA_ODT_PATH = os.path.join(BASE_DIR, 'plantillas_odt') #agregado basado en rango

def sigNumero(nombreNumerador):
	try:
		n = Numerador.objects.get(nombre=nombreNumerador)
	except Numerador.DoesNotExist:
		#Si no existe en la BD, lo creo
		n = Numerador(nombre=nombreNumerador, ultimo_valor = 1)
		n.save()
		return n.ultimo_valor
	else:
		#si existe, incremento el valor, lo guardo y lo retorno
		n.ultimo_valor += 1
		n.save()
		return n.ultimo_valor
	
def completarConCeros( numero, longitud):
	numerotxt = str(numero)
	return numerotxt.zfill(longitud)

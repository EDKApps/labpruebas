from .models import Numerador

def sigNumero(nombreNumerador):
	try:
		n = Numerador.objects.get(nombre=NombreNumerador)
	except Publisher.DoesNotExist:
		#Si no existe en la BD, lo creo
		n = Numerador(nombre=nombreNumerador, ultimo_valor = 1)
		n.save()
		return n.ultimo_valor
	else:
		#si existe, incremento el valor, lo guardo y lo retorno
		n.ultimo_valor += 1
		n.save()
		return n.ultimo_valor

#numerador, created = Numerador.objects.update_or_create(
#        identifier=identifier, defaults={"name": name}
#)
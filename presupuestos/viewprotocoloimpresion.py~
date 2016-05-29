# -*- encoding: utf-8 -*-
from django.http import HttpResponse
from appy.pod.renderer import Renderer
import labutiles
import tempfile
import os
from django.core.servers.basehttp import FileWrapper 
from django.core.files import File
import protocolo_impresion

def protocolo_imprimir(request, idot):
	#ruta de la plantilla
    plantilla_odt_path = os.path.join(labutiles.PLANTILLA_ODT_PATH,'protocolo_impresion.odt')
	#Necesito un nombre aleatorio en la carpeta de temporales
    file_odt_resultado = tempfile.NamedTemporaryFile(delete=True,prefix='proto_', suffix='.odt') 

    odt_resultado_path = file_odt_resultado.name #path al archivo de resultado
    file_odt_resultado.close() #Se debería eliminar el archivo	
	
    plantilla = protocolo_impresion.protocoloimpresion(idot)
	
    contexto = {"plantilla":plantilla}
    renderer = Renderer(plantilla_odt_path, contexto, odt_resultado_path)
    renderer.run()    	
    archivo_resultado = File(open(odt_resultado_path))
    wrapper = FileWrapper(archivo_resultado) 
    
    response = HttpResponse(wrapper, content_type='text/html')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(odt_resultado_path)
    response['Content-Length'] = os.path.getsize(odt_resultado_path)
    return response

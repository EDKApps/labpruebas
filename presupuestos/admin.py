from django.contrib import admin
from .models import Cliente
from .models import Presupuesto, Numerador
from .models import Tipo
from .models import Estado
from .models import Matriz
from .models import Familia
from .models import Parametro
from .models import Tecnica
from .models import Unidades
from .models import MatrizTecnicaLct
from .models import ParametroPrecio 
from .models import PerfilPrecio
from .models import PerfilPrecio_Parametro
from .models import Campania
from .models import Item
from .models import Plantillas_Impresion
from .models import Orden_trabajo
from .models import Ot_Estado
from .models import Ot_Item
from .models import Muestra_Estado
from .models import Muestra
from .models import Analisis
from .models import Subitem_parametro
from .models import Subitem_perfil

admin.site.register(Cliente)
admin.site.register(Presupuesto)
admin.site.register(Numerador)
admin.site.register(Estado)
admin.site.register(Tipo)
admin.site.register(Matriz)
admin.site.register(Familia)
admin.site.register(Parametro)
admin.site.register(Tecnica)
admin.site.register(Unidades)
admin.site.register(MatrizTecnicaLct)
admin.site.register(ParametroPrecio)
admin.site.register(PerfilPrecio)
admin.site.register(PerfilPrecio_Parametro)
admin.site.register(Campania)
admin.site.register(Item)
admin.site.register(Plantillas_Impresion)
admin.site.register(Orden_trabajo)
admin.site.register(Ot_Estado)
admin.site.register(Ot_Item)
admin.site.register(Muestra_Estado)
admin.site.register(Muestra)
admin.site.register(Analisis)
admin.site.register(Subitem_parametro)
admin.site.register(Subitem_perfil)


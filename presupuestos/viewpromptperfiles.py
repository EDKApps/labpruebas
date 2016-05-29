 # -- coding: utf-8 --
from django.forms import ModelForm
from django import forms
from django.forms import modelformset_factory
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from .models import PerfilPrecio, Item, Subitem_perfil
from django.db.models import Q #para OR en consultas
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

#Armo el formset
class PerfilPrecio_Form(ModelForm): 
	class Meta:
		model = PerfilPrecio
		fields= ['seleccionado']		

@csrf_exempt #solo en esta vista desactivar el control de Crsf
def promptperfiles(request, iditem):
    PerfilPrecioFormSet = modelformset_factory(PerfilPrecio, form = PerfilPrecio_Form, extra= 0)
    item = Item.objects.get(id=iditem) #item al que agregar los perfiles
    if request.method == 'POST':
        formset = PerfilPrecioFormSet(request.POST, request.FILES)
        if formset.is_valid():
            
	        
            for form in formset: #recorro los formularios
                if form.cleaned_data['seleccionado']: #Si el perfil está selecciondo lo agrego al ítem
                    unperfilprecio = form.instance #la instancia relacionada, como figura en la BD
                    subitem_perfil = Subitem_perfil.objects.create(
                        item = item,
                        itemperfil= unperfilprecio
                    )
                    subitem_perfil.save()
            #volver al ítem
            #return   
            return HttpResponseRedirect( reverse('presupuestos:itemsubitem_modificar', kwargs={'pk': iditem,}) )
    else:		
        #quiero filtrar por la matriz del ítem y otros criterios de búsqueda

        querysearch = request.GET.get('q')
        if querysearch is None:
			querysearch = '' #si es nulo le asigno la cadena vacia
			queryset=PerfilPrecio.objects.filter(matriz = item.matriz).order_by('nombre')
        else:
            queryset=PerfilPrecio.objects.filter(Q( matriz = item.matriz, nombre__icontains=querysearch)).order_by('nombre')
			
        paginator = Paginator(queryset, 50) #50 formularios por página, pedido explicito del cliente
        page = request.GET.get('page')
        try:
            objects =paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        page_query = queryset.filter(id__in=[object.id for object in objects])
        	
        formset = PerfilPrecioFormSet(queryset=page_query) 
        contexto = {"PerfilPrecioFormSet": formset, "iditem":iditem, "querysearch":querysearch,"objects": objects}
    return render_to_response("presupuestos/promptperfilprecio.html", 
                              contexto
                             )
	

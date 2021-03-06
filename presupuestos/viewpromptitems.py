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
from .models import Orden_trabajo, Ot_Item, Item, Ot_Estado
from django.db.models import Q #para OR en consultas
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

#Armo el formset
class Item_Form(ModelForm): 
	class Meta:
		model = Item
		fields= ['seleccionado']		

@csrf_exempt #solo en esta vista desactivar el control de Crsf
def promptitems(request, idot):
    ItemFormSet = modelformset_factory(Item, form = Item_Form, extra= 0)
    #item = Item.objects.get(id=iditem) #item al que agregar los parámetros
    ot = Orden_trabajo.objects.get(id=idot)
    if request.method == 'POST':
        formset = ItemFormSet(request.POST, request.FILES)
        if formset.is_valid():
            
	        
            for form in formset: #recorro los formularios
                if form.cleaned_data['seleccionado']: #Si el objeto está selecciondo lo agrego donde corresponde
                    unitem = form.instance #la instancia relacionada, como figura en la BD
                    estado_pendiente = Ot_Estado.objects.get(id=1)
                    orden_trabajo = Orden_trabajo.objects.get(id= idot)
                    ot_item = Ot_Item.objects.create(
                              orden_trabajo = orden_trabajo,item = unitem, estado = estado_pendiente)
                    ot_item.save()
            #volver al ítem
            #return   
            return HttpResponseRedirect( reverse('presupuestos:ot_item_modificar', kwargs={'pk': idot,}) )
    else:		
        #quiero filtrar por presupuesto y otros criterios de búsqueda

        querysearch = request.GET.get('q')
        if querysearch is None:
			querysearch = '' #si es nulo le asigno la cadena vacia
			queryset=Item.objects.filter(presupuesto = ot.presupuesto)
        else:
             queryset=Item.objects.filter(Q( presupuesto = ot.presupuesto, descripcion__icontains=querysearch)| 
                                                    Q( presupuesto = ot.presupuesto, matriz__nombre_matriz__icontains=querysearch))

        paginator = Paginator(queryset, 10) #10 formularios por página
        page = request.GET.get('page')
        try:
            objects =paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        page_query = queryset.filter(id__in=[object.id for object in objects])
        	
        formset = ItemFormSet(queryset=page_query) 
        contexto = {"ItemFormSet": formset, "idot":idot,  "querysearch":querysearch,"objects": objects}
    return render_to_response("presupuestos/promptitem.html", contexto)
	

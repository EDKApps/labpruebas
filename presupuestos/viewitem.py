 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas

from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
item_fields = ('numero','descripcion','matriz','cantidadMuestra',)

from .models import Item


class ItemListar(ListView):
    model = Item
    paginate_by = 10
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Item.objects.all().order_by('-presupuesto')
        else:
            return Item.objects.filter( Q(descripcion__icontains=query) | 
                                       Q(matriz__nombre_matriz__icontains=query)| 
									  Q(presupuesto__referencia__icontains=query)).order_by('-presupuesto')
            #return Item.objects.all().order_by('presupuesto')
        
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(ItemListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context    
    
class ItemCrear(CreateView):
    model = Item
    fields = item_fields
	
    def get_success_url(self):
        return reverse('presupuestos:item_detalle', kwargs={
            'pk': self.object.pk,
        })

class ItemDetalle(DetailView):
    model = Item
    fields = item_fields

class ItemModificar(UpdateView):
    model = Item
    fields = item_fields
	
    def get_success_url(self):
        return reverse('presupuestos:item_detalle', kwargs={
            'pk': self.object.pk,
        })

class ItemBorrar(DeleteView):
    model = Item
    success_url = reverse_lazy('presupuestos:item_listar')
    fields = item_fields
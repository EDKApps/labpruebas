 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas
from django.db.models.deletion import ProtectedError

from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
import json

familia_fields = ('nombre',)

from .models import Familia

class FamiliaListar(ListView):
    model = Familia
    paginate_by = 10
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Familia.objects.all()
        else:
            return Familia.objects.filter( Q(nombre__icontains=query) )
                                  
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(FamiliaListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context    
    
class FamiliaCrear(CreateView):
    model = Familia
    fields = familia_fields
	
    def get_success_url(self):
        return reverse('presupuestos:familia_confirma_alta', kwargs={
            'pk': self.object.pk,
        })

class FamiliaDetalle(DetailView):
    model = Familia
    fields = familia_fields

class FamiliaConfirmaAlta(DetailView):
    template_name = 'presupuestos/familia_confirm_create.html'
    model = Familia
    fields = familia_fields
    
class FamiliaModificar(UpdateView):
    model = Familia
    fields = familia_fields
	
    def get_success_url(self):
        return reverse('presupuestos:familia_detalle', kwargs={
            'pk': self.object.pk,
        })

class FamiliaBorrar(DeleteView):
    model = Familia
    success_url = reverse_lazy('presupuestos:familia_listar')
    fields = familia_fields
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            data = {'success':'ok'}
        except ProtectedError:
            data = {'success':'violation_protected'}
        #return HttpResponse(json.dumps(data),mimetype="application/json")    
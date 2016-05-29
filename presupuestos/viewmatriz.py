 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q #para OR en consultas
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError


from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
import json
matriz_fields = ('nombre_matriz',)

from .models import Matriz


class MatrizListar(ListView):
    model = Matriz
    paginate_by = 10
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Matriz.objects.all().order_by('nombre_matriz')
        else:
            return Matriz.objects.filter( Q(nombre_matriz__icontains=query)).order_by('nombre_matriz')
                                  
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(MatrizListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context    
    
class MatrizCrear(CreateView):
    model = Matriz
    fields = matriz_fields
	
    def get_success_url(self):
        return reverse('presupuestos:matriz_detalle', kwargs={
            'pk': self.object.pk,
        })

class MatrizDetalle(DetailView):
    model = Matriz
    fields = matriz_fields

class MatrizModificar(UpdateView):
    model = Matriz
    fields = matriz_fields
	
    def get_success_url(self):
        return reverse('presupuestos:matriz_detalle', kwargs={
            'pk': self.object.pk,
        })

class MatrizBorrar(DeleteView):
    model = Matriz
    success_url = reverse_lazy('presupuestos:matriz_listar')
    fields = matriz_fields
    
    def delete(self, request, *args, **kwargs):
        matriz = self.get_object()
        
        try:
            matriz.delete()
            estado = 'Matriz eliminada correctamente'
        except ValidationError as e:
            estado = 'Objeto protegido.' + str(e) 
        respuesta = estado
        
        return render(request, 'presupuestos/confirmar_borrado_matriz.html',{"respuesta":respuesta })
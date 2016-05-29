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

parametro_fields = ('nombre_par','familia')

from .models import Parametro, Familia

class ParametroListar(ListView):
    model = Parametro
    paginate_by = 10
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Parametro.objects.all().order_by('nombre_par')
        else:
            return Parametro.objects.filter( Q(nombre_par__icontains=query)).order_by('nombre_par')
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(ParametroListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context    

#Listado con paginado de 2000, osea, seria como sin paginado
class ParametroListarVisualizar(ListView):
    model = Parametro
    paginate_by = 2000
    template_name = 'presupuestos/parametro_list_visualizar.html'
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Parametro.objects.all().order_by('nombre_par')
        else:
            return Parametro.objects.filter( Q(nombre_par__icontains=query)).order_by('nombre_par')
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(ParametroListarVisualizar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context
    
class ParametroCrear(CreateView):
    model = Parametro
    fields = parametro_fields
	
    def get_success_url(self):
        return reverse('presupuestos:parametro_detalle', kwargs={
            'pk': self.object.pk,
        })
    
    def get_form(self, form_class):
        form = super(ParametroCrear, self).get_form(form_class)
        form.fields['familia'] = forms.ModelChoiceField(queryset = Familia.objects.order_by('nombre'))
        return form

class ParametroDetalle(DetailView):
    model = Parametro
    fields = parametro_fields

class ParametroModificar(UpdateView):
    model = Parametro
    fields = parametro_fields
	
    def get_success_url(self):
        return reverse('presupuestos:parametro_detalle', kwargs={
            'pk': self.object.pk,
        })
    
    def get_form(self, form_class):
        form = super(ParametroModificar, self).get_form(form_class)
        form.fields['familia'] = forms.ModelChoiceField(queryset = Familia.objects.order_by('nombre'))
        return form

class ParametroBorrar(DeleteView):
    model = Parametro
    success_url = reverse_lazy('presupuestos:parametro_listar')
    fields = parametro_fields
    
    def delete(self, request, *args, **kwargs):
        parametro = self.get_object()
        
        try:
            parametro.delete()
            estado = 'Parametro eliminado correctamente'
        except ValidationError as e:
            estado = 'Objeto protegido.' + str(e) 
        respuesta = estado
        
        return render(request, 'presupuestos/confirmar_borrado_parametro.html',{"respuesta":respuesta })
        #return HttpResponse(respuesta   )    

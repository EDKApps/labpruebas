 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q #para OR en consultas
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError

from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
import json

parametroprecio_fields = ('matriz','parametro','tecnica','precio_parametro','fecha_precio','fuente_precio')

from .models import ParametroPrecio, Matriz, Parametro, Tecnica

class ParametroPrecioListar(ListView):
    model = ParametroPrecio
    paginate_by = 10
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return ParametroPrecio.objects.all().order_by('matriz__nombre_matriz', 'parametro__nombre_par', 'tecnica__nombre_tec')
        else:
            return ParametroPrecio.objects.filter( Q(parametro__nombre_par__icontains=query)).order_by('matriz__nombre_matriz', 'parametro__nombre_par', 'tecnica__nombre_tec')

    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(ParametroPrecioListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context    

#Listado con paginado de 2000, osea, seria como sin paginado
class ParametroPrecioListarVisualizar(ListView):
    model = ParametroPrecio
    paginate_by = 2000
    template_name = "presupuestos/parametroprecio_list_visualizar.html"

    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return ParametroPrecio.objects.all().order_by('matriz__nombre_matriz', 'parametro__nombre_par', 'tecnica__nombre_tec')
        else:
            return ParametroPrecio.objects.filter( Q(parametro__nombre_par__icontains=query)).order_by('matriz__nombre_matriz', 'parametro__nombre_par', 'tecnica__nombre_tec')

    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(ParametroPrecioListarVisualizar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context    
    
class ParametroPrecioCrear(CreateView):
    model = ParametroPrecio
    fields = parametroprecio_fields
	
    def get_success_url(self):
        return reverse('presupuestos:parametroprecio_detalle', kwargs={
            'pk': self.object.pk,
        })

    def get_form(self, form_class):
        form = super(ParametroPrecioCrear, self).get_form(form_class)
        form.fields['matriz'] = forms.ModelChoiceField(queryset = Matriz.objects.order_by('nombre_matriz'))
        form.fields['parametro'] = forms.ModelChoiceField(queryset = Parametro.objects.order_by('nombre_par'))
        form.fields['tecnica'] = forms.ModelChoiceField(queryset = Tecnica.objects.order_by('nombre_tec'))
        return form

class ParametroPrecioDetalle(DetailView):
    model = ParametroPrecio
    fields = parametroprecio_fields

class ParametroPrecioModificar(UpdateView):
    model = ParametroPrecio
    fields = parametroprecio_fields
	
    def get_success_url(self):
        return reverse('presupuestos:parametroprecio_detalle', kwargs={
            'pk': self.object.pk,
        })
    def get_form(self, form_class):
        form = super(ParametroPrecioModificar, self).get_form(form_class)
        form.fields['matriz'] = forms.ModelChoiceField(queryset = Matriz.objects.order_by('nombre_matriz'))
        form.fields['parametro'] = forms.ModelChoiceField(queryset = Parametro.objects.order_by('nombre_par'))
        form.fields['tecnica'] = forms.ModelChoiceField(queryset = Tecnica.objects.order_by('nombre_tec'))
        return form

class ParametroPrecioBorrar(DeleteView):
    model = ParametroPrecio
    success_url = reverse_lazy('presupuestos:parametroprecio_listar')
    fields = parametroprecio_fields
    
    def delete(self, request, *args, **kwargs):
        parametroprecio = self.get_object()
        
        try:
            parametroprecio.delete()
            estado = 'Precio de Parametro eliminado correctamente'
        except ValidationError as e:
            estado = 'Objeto protegido.' + str(e)
        respuesta = estado
        
        return render(request, 'presupuestos/confirmar_borrado_precio_parametro.html',{"respuesta":respuesta })

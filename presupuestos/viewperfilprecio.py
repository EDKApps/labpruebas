 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q #para OR en consultas
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
import json
#perfilprecio_fields = ('nombre','matriz','perfil','tecnica','fecha_precio','fuente_precio')

from .formperfilprecio import PerfilPrecioForm, PerfilPrecio_ParametroFormSet
from .models import PerfilPrecio, PerfilPrecio_Parametro, Matriz, Parametro, Tecnica

class PerfilPrecioListar(ListView):
    model = PerfilPrecio
    paginate_by = 10
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return PerfilPrecio.objects.all().order_by('nombre')
        else:
            return PerfilPrecio.objects.filter (Q(nombre__icontains=query) | 
				                          Q(matriz__nombre_matriz__icontains=query)).order_by('nombre')    
        
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(PerfilPrecioListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context

#Listado con paginado de 2000, osea, seria como sin paginado
class PerfilPrecioListarVisualizar(ListView):
    model = PerfilPrecio
    paginate_by = 2000
    template_name = 'presupuestos/perfilprecio_list_visualizar.html'

    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return PerfilPrecio.objects.all().order_by('nombre')
        else:
            return PerfilPrecio.objects.filter (Q(nombre__icontains=query) | 
				                          Q(matriz__nombre_matriz__icontains=query)).order_by('nombre')    
        
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(PerfilPrecioListarVisualizar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context    
    
class PerfilPrecioCrear(CreateView):
    model = PerfilPrecio
    form_class= PerfilPrecioForm

    def get_success_url(self):
        return reverse('presupuestos:perfilprecio_confirma_alta', kwargs={
            'pk': self.object.pk,
        })

    #ordenar los combos, opciones.
    def get_form(self, form_class):
        form = super(PerfilPrecioCrear, self).get_form(form_class)
        form.fields['matriz'] = forms.ModelChoiceField(queryset = Matriz.objects.order_by('nombre_matriz'))

        #ordenar los combos del inline, todo
        """
        parametro_form = PerfilPrecio_ParametroFormSet()
        parametro_form.fields['parametro'] = forms.ModelChoiceField(queryset = Parametro.objects.order_by('nombre_par'))
        """
        return form

    def get(self, request, *args, **kwargs):
        """
        Maneja GET requests e instancia una versión limpia del form y su formset
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        parametro_form = PerfilPrecio_ParametroFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  parametro_form=parametro_form,
                                  ))
    def post(self, request, *args, **kwargs):        
        """
        Maneja POST request instanciando un form con sus formsets,
        con las variables POST pasadas y chequea validez
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        parametro_form = PerfilPrecio_ParametroFormSet(self.request.POST)
        if (form.is_valid() and parametro_form.is_valid()):
            return self.form_valid(form, parametro_form)
        else:
            return self.form_invalid(form, parametro_form)
    
    def form_valid(self, form, parametro_form):
        """
        Llamada si todos los forms son válidos. Crea cabecera junto con
        los parámetros asociados y redirecciona a una página de éxito
        """
        self.object = form.save()
        parametro_form.instance = self.object
        parametro_form.save()
        return HttpResponseRedirect(self.get_success_url())
            
    def form_invalid(self, form, parametro_form):
        """
        Llamada si un formulario es inválido. Re-renders context data con el formulario
        cargado y los errores
        """
        return self.render_to_response(
                self.get_context_data(form=form,
                                      parametro_form = parametro_form))
            
class PerfilPrecioDetalle(DetailView):
    model = PerfilPrecio
    #fields = perfilprecio_fields

class PerfilPrecioConfirmaAlta(DetailView):
    template_name = 'presupuestos/perfilprecio_confirm_create.html'
    model = PerfilPrecio
    #fields = perfilprecio_fields

    
class PerfilPrecioModificar(UpdateView):
    model = PerfilPrecio
    form_class= PerfilPrecioForm

    #ordenar los combos, opciones.
    def get_form(self, form_class):
        form = super(PerfilPrecioModificar, self).get_form(form_class)
        form.fields['matriz'] = forms.ModelChoiceField(queryset = Matriz.objects.order_by('nombre_matriz'))
        return form
    
    def get(self, request, *args, **kwargs):
        """
        Maneja GET requests e instancia una versión limpia del form y su formset
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #obtener parametros
        #parametros = PerfilPrecio_Parametro.objects.filter(perfilprecio=self.object).values() #.order_by('name').values()
        
        #render form
        parametro_form = PerfilPrecio_ParametroFormSet(instance = self.object) #antes (initial = parametros)
        
        return self.render_to_response(
            self.get_context_data(form=form,
                                  parametro_form=parametro_form,
                                  ))
    
    def post(self, request, *args, **kwargs):        
        """
        Maneja POST request instanciando un form con sus formsets,
        con las variables POST pasadas y chequea validez
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #parametro_form = PerfilPrecio_ParametroFormSet(self.request.POST)
        
        parametro_form = PerfilPrecio_ParametroFormSet(request.POST,request.FILES,instance= self.object )
        
        if (form.is_valid() and parametro_form.is_valid()):

            
            self.object = form.save(commit=False)
            
            self.object.save()
            parametro_form.save()
            #Eliminar lo indicado del subnivel
            #PerfilPrecio_Parametro.objects.filter(perfilprecio=self.object, eliminado = True).delete()
            return HttpResponseRedirect(self.get_success_url())
            
            
        else:
            return self.form_invalid(form, parametro_form)
    
    def get_success_url(self):
        return reverse('presupuestos:perfilprecio_detalle', kwargs={
            'pk': self.object.pk,
        })
            
    def form_invalid(self, form, parametro_form):
        """
        Llamada si un formulario es inválido. Re-renders context data con el formulario
        cargado y los errores
        """
        return self.render_to_response(
                self.get_context_data(form=form,
                                      parametro_form = parametro_form))

class PerfilPrecioBorrar(DeleteView):
    model = PerfilPrecio
    success_url = reverse_lazy('presupuestos:perfilprecio_listar')
    
    def delete(self, request, *args, **kwargs):
        perfilPrecio = self.get_object()
        
        try:
            perfilPrecio.delete()
            estado = 'Precio del Perfil eliminado correctamente'
        except ValidationError as e:
            estado = 'Objeto protegido.' + str(e) 
        respuesta = estado
        
        return render(request, 'presupuestos/confirmar_borrado_perfil_precio.html',{"respuesta":respuesta })

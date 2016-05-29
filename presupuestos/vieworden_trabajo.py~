 # -- coding: utf-8 --
from django import forms
#from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q #para OR en consultas
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError

from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.extras.widgets import SelectDateWidget
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
import json

#En el form de alta excluyo la referencia (automática)
ot_fields_full = ('presupuesto','referencia_clave', 'referencia', 'descripcion', 'prioridad', 'fecha_creacion')
ot_fields_crear = ('presupuesto','referencia_clave', 'descripcion', 'prioridad', 'fecha_creacion')
ot_fields_modif = ('referencia_clave', 'referencia', 'descripcion', 'prioridad', 'fecha_creacion')

from .models import Orden_trabajo, Presupuesto

class Orden_trabajoListar(ListView):
    paginate_by = 10

    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Orden_trabajo.objects.all().order_by('-referencia')
        else:
            return Orden_trabajo.objects.filter( Q(referencia_clave__icontains=query) | 
                                           Q(referencia__icontains=query) |
                                           Q(descripcion__icontains=query) |
                                           Q(prioridad__icontains=query)).order_by('-referencia')

    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(Orden_trabajoListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context    
	
class Orden_trabajoFormCrear(forms.ModelForm):
    class Meta:
        #Provee una asociación entre el ModelForm y un model
        model = Orden_trabajo
        fields = ot_fields_crear	

class Orden_trabajoFormModificar(forms.ModelForm):
    #referencia = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        #Provee una asociación entre el ModelForm y un model
        model = Orden_trabajo
        fields = ot_fields_modif	

		
class Orden_trabajoCrear(CreateView):
    model = Orden_trabajo
    form_class = Orden_trabajoFormCrear

    def get_success_url(self):
        return reverse('presupuestos:orden_trabajo_detalle', kwargs={
            'pk': self.object.pk,
        })
    def get_form(self, form_class):
        form = super(Orden_trabajoCrear, self).get_form(form_class)
        form.fields['presupuesto'] = forms.ModelChoiceField(queryset = Presupuesto.objects.order_by('-referencia'))
        return form
	
class Orden_trabajoDetalle(DetailView):
    model = Orden_trabajo
    fields = ot_fields_modif

class Orden_trabajoModificar(UpdateView):
    model = Orden_trabajo
    form_class = Orden_trabajoFormModificar
    template_name = 'presupuestos/orden_trabajo_form_mod.html'
	
    def get_success_url(self):
        return reverse('presupuestos:orden_trabajo_detalle', kwargs={
            'pk': self.object.pk,
        })

class Orden_trabajoBorrar(DeleteView):
    model = Orden_trabajo
    success_url = reverse_lazy('presupuestos:orden_trabajo_listar')
    fields = ot_fields_modif
    
    def delete(self, request, *args, **kwargs):
        orden_trabajo = self.get_object()
        
        try:
            orden_trabajo.delete()
            estado = 'Orden de trabajo eliminada correctamente'
        except ValidationError as e:
            estado = 'Objeto protegido.' + str(e)
        respuesta = estado
        return render(request, 'presupuestos/confirmar_borrado.html',{"respuesta":respuesta })

	

class Orden_trabajoDetalleFull(DetailView):
    model = Orden_trabajo
    fields = ot_fields_full
    template_name = 'presupuestos/orden_trabajo_detail_full.html'

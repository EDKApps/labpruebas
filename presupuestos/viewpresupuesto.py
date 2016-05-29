 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.extras.widgets import SelectDateWidget
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.db.models import Q #para OR en consultas
from .models import Presupuesto, Item, Campania, Cliente, Tipo, Estado
import json

#En el form de alta excluyo la referencia (automática)
presupuesto_fields_full = ('cliente','referencia_clave', 'referencia', 'tipo', 'fecha_solicitud', 'fecha_vencimiento', 'fecha_envio', 'fecha_aprobacion', 'descripcion', 'estado', 'observacion','item.numero')
presupuesto_fields_crear = ('cliente','referencia_clave', 'tipo', 'fecha_solicitud', 'fecha_vencimiento', 'fecha_envio', 'fecha_aprobacion', 'descripcion', 'estado', 'observacion', 'descuento')
presupuesto_fields_modif = ('cliente','referencia_clave', 'referencia', 'tipo', 'fecha_solicitud', 'fecha_vencimiento', 'fecha_envio', 'fecha_aprobacion', 'descripcion', 'estado', 'observacion', 'descuento')
fecha_solicitud_anios = ('2015', '2016', '2017')
#from .models import Presupuesto, Item, Campania

#Presupuesto
class PresupuestoListar( ListView):
    model = Presupuesto
    paginate_by = 10
	#context_object_name = 'lista_de_presupuestos' #opcion a object_list
    #búsqueda

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query is None:
            return Presupuesto.objects.all().order_by('-referencia')
        else:
            return Presupuesto.objects.filter( Q(referencia_clave__icontains=query) |
                                           Q(referencia__icontains=query) |
                                           Q(cliente__empresa__icontains=query) |
										  Q(estado__estado_actual__icontains=query)).order_by('-referencia')

    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(PresupuestoListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context

class PresupuestoFormCrear(forms.ModelForm):
    class Meta:
        #Provee una asociación entre el ModelForm y un model
        model = Presupuesto
        fields = presupuesto_fields_crear

class PresupuestoFormModificar(forms.ModelForm):
    referencia = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        #Provee una asociación entre el ModelForm y un model
        model = Presupuesto
        fields = presupuesto_fields_modif

class PresupuestoCrear(CreateView):
    model = Presupuesto
    form_class = PresupuestoFormCrear

    def get_success_url(self):
        return reverse('presupuestos:presupuesto_detalle', kwargs={
            'pk': self.object.pk,
        })

    def get_form(self, form_class):
        form = super(PresupuestoCrear, self).get_form(form_class)
        form.fields['cliente'] = forms.ModelChoiceField(queryset = Cliente.objects.order_by('contacto'))
        form.fields['tipo'] = forms.ModelChoiceField(queryset = Tipo.objects.order_by('nombre_tipo'))
        form.fields['estado'] = forms.ModelChoiceField(queryset = Estado.objects.order_by('estado_actual'))
        return form

class PresupuestoDetalle(DetailView):
    model = Presupuesto
    fields = presupuesto_fields_modif

class PresupuestoModificar(UpdateView):
    model = Presupuesto
    #fields = presupuesto_fields
    form_class = PresupuestoFormModificar

    def get_success_url(self):
        return reverse('presupuestos:presupuesto_detalle', kwargs={
            'pk': self.object.pk,
        })
    def get_form(self, form_class):
        form = super(PresupuestoModificar, self).get_form(form_class)
        form.fields['cliente'] = forms.ModelChoiceField(queryset = Cliente.objects.order_by('contacto'))
        form.fields['tipo'] = forms.ModelChoiceField(queryset = Tipo.objects.order_by('nombre_tipo'))
        form.fields['estado'] = forms.ModelChoiceField(queryset = Estado.objects.order_by('estado_actual'))
        return form

class PresupuestoBorrar(DeleteView):
    model = Presupuesto
    success_url = reverse_lazy('presupuestos:presupuesto_listar')
    fields = presupuesto_fields_modif

    def delete(self, request, *args, **kwargs):
        presupuesto = self.get_object()

        try:
            presupuesto.delete()
            estado = 'Presupuesto eliminado correctamente'
        except ValidationError as e:
            estado = 'Objeto protegido.' + str(e)
        respuesta = estado

        return render(request, 'presupuestos/confirmar_borrado.html',{"respuesta":respuesta })

class PresupuestoDetalleFull(DetailView):
    model = Presupuesto
    fields = presupuesto_fields_full
    template_name = 'presupuestos/presupuesto_detail_full.html'

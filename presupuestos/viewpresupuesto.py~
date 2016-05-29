 # -- coding: utf-8 --
from django import forms
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.extras.widgets import SelectDateWidget
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.db.models import Q #para OR en consultas
from .models import Presupuesto, Item, Campania

#En el form de alta excluyo la referencia (automática)
presupuesto_fields_full = ('cliente','referencia_clave', 'referencia', 'tipo', 'fecha_solicitud', 'fecha_vencimiento', 'fecha_envio', 'fecha_aprobacion', 'descripcion', 'estado', 'observacion','item.numero')

presupuesto_fields_crear = ('cliente','referencia_clave', 'tipo', 'fecha_solicitud', 'fecha_vencimiento', 'fecha_envio', 'fecha_aprobacion', 'descripcion', 'estado', 'observacion', 'descuento')
presupuesto_fields_modif = ('cliente','referencia_clave', 'referencia', 'tipo', 'fecha_solicitud', 'fecha_vencimiento', 'fecha_envio', 'fecha_aprobacion', 'descripcion', 'estado', 'observacion', 'descuento')
fecha_solicitud_anios = ('2015', '2016', '2017')
#from .models import Presupuesto, Item, Campania

#Presupuesto
class PresupuestoListar(ListView):
    model = Presupuesto
    paginate_by = 10
	#context_object_name = 'lista_de_presupuestos' #opcion a object_list
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Presupuesto.objects.all()
        else:
            return Presupuesto.objects.filter( Q(referencia_clave__icontains=query) | 
                                           Q(referencia__icontains=query) |
                                           Q(cliente__empresa__icontains=query) )
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

class PresupuestoBorrar(DeleteView):
    model = Presupuesto
    success_url = reverse_lazy('presupuestos:presupuesto_listar')
    fields = presupuesto_fields_modif
	
class PresupuestoDetalleFull(DetailView):
    model = Presupuesto
    fields = presupuesto_fields_full
    template_name = 'presupuestos/presupuesto_detail_full.html'

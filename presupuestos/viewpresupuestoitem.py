 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, DetailView

from .formpresupuestoitem import PresupuestoForm, Presupuesto_ItemFormSet
from .models import Presupuesto, Item

presupuesto_fields = ('cliente','referencia_clave', 'referencia', 'tipo', 'fecha_solicitud', 'fecha_vencimiento', 'fecha_envio', 'fecha_aprobacion', 'descripcion', 'estado', 'observacion', 'descuento')

class PresupuestoItemFormModificar(forms.ModelForm):
    referencia = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        #Provee una asociación entre el ModelForm y un model
        model = Presupuesto
        fields = presupuesto_fields
    
class PresupuestoItemModificar(UpdateView):
    template_name = 'presupuestos/presupuestoitem_form.html'
    model = Presupuesto
    form_class = PresupuestoItemFormModificar
    success_url = reverse_lazy('presupuestos:presupuesto_listar')
    
    def get(self, request, *args, **kwargs):
        """
        Maneja GET requests e instancia una versión limpia del form y su formset
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)        
        #render form 
        #item_form = Presupuesto_ItemFormSet(instance = self.object)
        item_form = Presupuesto_ItemFormSet(instance = self.object, #self.object es el parent object
											queryset= (self.object).item_set.order_by("numero"))
        
        return self.render_to_response(
            self.get_context_data(form=form,
                                  item_form=item_form,
                                  ))
    
    def post(self, request, *args, **kwargs):        
        """
        Maneja POST request instanciando un form con sus formsets,
        con las variables POST pasadas y chequea validez
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        item_form = Presupuesto_ItemFormSet(request.POST,request.FILES,instance= self.object )
        
        if (form.is_valid() and item_form.is_valid()):

            
            self.object = form.save(commit=False)
            
            self.object.save()
            item_form.save()
            #Eliminar lo indicado del subnivel
            #PerfilPrecio_Parametro.objects.filter(perfilprecio=self.object, eliminado = True).delete()
            return HttpResponseRedirect(self.get_success_url())
            
        else:
            return self.form_invalid(form, item_form)
    
    #def get_success_url(self):
    #    return reverse('presupuestos:presupuesto_listar', kwargs={
    #        'pk': self.object.pk,
    #    }) 
            
    def form_invalid(self, form, item_form):
        """
        Llamada si un formulario es inválido. Re-renders context data con el formulario
        cargado y los errores
        """
        return self.render_to_response(
                self.get_context_data(form=form,
                                      item_form = item_form))

class PresupuestoItemDetalle(DetailView):
    template_name = 'presupuestos/presupuestoitem_detail.html'    
    model = Presupuesto
    fields = '__all__'
    

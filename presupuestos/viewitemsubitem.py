 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, DetailView
presupuesto_fields = '__all__'

from .formitemsubitem import ItemForm, Subitem_parametroFormSet, Subitem_perfilFormSet
from .models import Item, Subitem_parametro, Subitem_perfil
    
class ItemSubitemModificar(UpdateView):
    template_name = 'presupuestos/itemsubitem_form.html'
    model = Item
    form_class= ItemForm
    #dfd success_url = reverse_lazy('presupuestos:presupuestoitem_detalle')
   
    def get_success_url(self):
        return reverse('presupuestos:presupuestoitem_detalle', kwargs={
            'pk': self.object.presupuesto.pk,
        })    
    
    def get(self, request, *args, **kwargs):
        """
        Maneja GET requests e instancia una versión limpia del form y su formset
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)        
        #render form 
        subitem_parametro_form = Subitem_parametroFormSet(instance = self.object)
        subitem_perfil_form    = Subitem_perfilFormSet(instance = self.object)
        
        return self.render_to_response(
            self.get_context_data(form=form,
                                  subitem_parametro_form=subitem_parametro_form,
                                  subitem_perfil_form = subitem_perfil_form))
    
    def post(self, request, *args, **kwargs):        
        """
        Maneja POST request instanciando un form con sus formsets,
        con las variables POST pasadas y chequea validez
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)   
        
        #subitem-parametro
        subitem_parametro_form = Subitem_parametroFormSet(instance = Item())
        subitem_parametro_form = Subitem_parametroFormSet(request.POST, request.FILES, instance = self.object)
        #subitem-perfil
        subitem_perfil_form = Subitem_perfilFormSet(instance = Item())
        subitem_perfil_form = Subitem_perfilFormSet(request.POST, request.FILES, instance = self.object)
        
        if (form.is_valid() and subitem_parametro_form.is_valid() and subitem_perfil_form.is_valid()):

            
            self.object = form.save(commit=False)
            
            self.object.save()
            subitem_parametro_form.save()
            subitem_perfil_form.save()
            #Eliminar lo indicado del subnivel
            #PerfilPrecio_Parametro.objects.filter(perfilprecio=self.object, eliminado = True).delete()
            return HttpResponseRedirect(self.get_success_url())
            
        else:
            return self.form_invalid(form, subitem_parametro_form, subitem_perfil_form)
    
    #def get_success_url(self):
    #    return reverse('presupuestos:presupuesto_listar', kwargs={
    #        'pk': self.object.pk,
    #    }) 
            
    def form_invalid(self, form, subitem_parametro_form, subitem_perfil_form):
        """
        Llamada si un formulario es inválido. Re-renders context data con el formulario
        cargado y los errores
        """
        return self.render_to_response(
                self.get_context_data(form=form,
                                      subitem_parametro_form = subitem_parametro_form,
                                      subitem_perfil_form = subitem_perfil_form ))

#class PresupuestoItemDetalle(DetailView):
#   template_name = 'presupuestos/presupuestoitem_detail.html'    
#    model = Presupuesto
#    fields = '__all__'
    
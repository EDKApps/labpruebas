 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, DetailView
presupuesto_fields = '__all__'

from .formpresupuestocampania import PresupuestoForm, Presupuesto_CampaniaFormSet
from .models import Presupuesto, Campania
    
class PresupuestoCampaniaModificar(UpdateView):
    template_name = 'presupuestos/presupuestocampania_form.html'
    model = Presupuesto
    form_class= PresupuestoForm
    success_url = reverse_lazy('presupuestos:presupuesto_listar')
    
    def get(self, request, *args, **kwargs):
        """
        Maneja GET requests e instancia una versión limpia del form y su formset
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)        
        #render form 
        campania_form = Presupuesto_CampaniaFormSet(instance = self.object)
        
        return self.render_to_response(
            self.get_context_data(form=form,
                                  campania_form=campania_form,
                                  ))
    
    def post(self, request, *args, **kwargs):        
        """
        Maneja POST request instanciando un form con sus formsets,
        con las variables POST pasadas y chequea validez
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        campania_form = Presupuesto_CampaniaFormSet(instance = Presupuesto())
        campania_form = Presupuesto_CampaniaFormSet(request.POST,request.FILES,instance= self.object )
        
        if (form.is_valid() and campania_form.is_valid()):

            
            self.object = form.save(commit=False)
            
            self.object.save()
            campania_form.save()
            #Eliminar lo indicado del subnivel
            #PerfilPrecio_Parametro.objects.filter(perfilprecio=self.object, eliminado = True).delete()
            return HttpResponseRedirect(self.get_success_url())
            
        else:
            return self.form_invalid(form, campania_form)
    
    #def get_success_url(self):
    #    return reverse('presupuestos:presupuesto_listar', kwargs={
    #        'pk': self.object.pk,
    #    }) 
            
    def form_invalid(self, form, campania_form):
        """
        Llamada si un formulario es inválido. Re-renders context data con el formulario
        cargado y los errores
        """
        return self.render_to_response(
                self.get_context_data(form=form,
                                      campania_form = campania_form))
#
#class PresupuestoCampaniaDetalle(DetailView):
#    template_name = 'presupuestos/presupuestoCampania_detail.html'    
#    model = Presupuesto
#    fields = '__all__'
    

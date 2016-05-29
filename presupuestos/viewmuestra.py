 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, DetailView, ListView

from .formmuestra_ot_item import Muestra_Ot_ItemFormSet 
from .models import Muestra, Ot_Item

ot_item_fields = ('numero', 'estado')

class Muestra_Ot_ItemFormModificar(forms.ModelForm):

    #hacer que numero no sea editable

    class Meta:
        #Provee una asociación entre el ModelForm y un model
        model = Ot_Item
        fields = ot_item_fields

class Muestra_Ot_ItemModificar(UpdateView):
    template_name = 'presupuestos/muestra_ot_item_form.html'
    model = Ot_Item
    form_class = Muestra_Ot_ItemFormModificar
    success_url = reverse_lazy('presupuestos:muestra_ot_item_listar')
    
    def get(self, request, *args, **kwargs):
        """
        Maneja GET requests e instancia una versión limpia del form y su formset
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)        
        #render form 
        muestra_form = Muestra_Ot_ItemFormSet(instance = self.object)
        
        return self.render_to_response(
            self.get_context_data(form=form,
                                  muestra_form=muestra_form,
                                  ))
    
    def post(self, request, *args, **kwargs):        
        """
        Maneja POST request instanciando un form con sus formsets,
        con las variables POST pasadas y chequea validez
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        
        muestra_form = Muestra_Ot_ItemFormSet(instance = Ot_Item())
        muestra_form = Muestra_Ot_ItemFormSet(request.POST,request.FILES,instance= self.object )
        
        if (form.is_valid() and muestra_form.is_valid()):

            
            self.object = form.save(commit=False)
            
            self.object.save()
            muestra_form.save()
            #Eliminar lo indicado del subnivel
            return HttpResponseRedirect(self.get_success_url())
            
        else:
            return self.form_invalid(form, muestra_form)
                
    def form_invalid(self, form, muestra_form):
        """
        Llamada si un formulario es inválido. Re-renders context data con el formulario
        cargado y los errores
        """
        return self.render_to_response(
                self.get_context_data(form=form,
                                      muestra_form = muestra_form))

class Muestra_Ot_Item_Listar(ListView):
    template_name = 'presupuestos/muestra_ot_item_list.html'
    paginate_by = 10
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Ot_Item.objects.order_by('-orden_trabajo','numero')
        else:
            return Ot_Item.objects.filter( Q(numero__icontains=query)| 
                                           Q(orden_trabajo__referencia__icontains=query) | 
                                           Q(item__matriz__nombre_matriz__icontains=query) | 
                                           Q(estado__estado_actual__icontains=query)).order_by('-orden_trabajo','numero')
                                  
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(Muestra_Ot_Item_Listar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context    


class Muestra_Listar(ListView):
    paginate_by = 50
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Muestra.objects.order_by('-referencia')
        else:
            return Muestra.objects.filter( Q(referencia__icontains=query)| 
                                           Q(ot_item__orden_trabajo__referencia__icontains=query) | 
                                           Q(ot_item__item__matriz__nombre_matriz__icontains=query) | 
                                           Q(estado__estado_actual__icontains=query)).order_by('-referencia')
                                  
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(Muestra_Listar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context

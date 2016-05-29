 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import UpdateView, DetailView, ListView

from .formotitem import Orden_trabajoForm, Orden_trabajo_Ot_ItemFormSet
from .models import Orden_trabajo, Ot_Item

orden_trabajo_fields = ('referencia_clave', 'referencia', 'descripcion', 'prioridad')

class Orden_trabajoOt_ItemFormModificar(forms.ModelForm):
    referencia = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        #Provee una asociación entre el ModelForm y un model
        model = Orden_trabajo
        fields = orden_trabajo_fields
    
class Ot_ItemModificar(UpdateView):
    template_name = 'presupuestos/otitem_form.html'
    model = Orden_trabajo
    form_class = Orden_trabajoOt_ItemFormModificar
    success_url = reverse_lazy('presupuestos:orden_trabajo_listar')
    
    def get(self, request, *args, **kwargs):
        """
        Maneja GET requests e instancia una versión limpia del form y su formset
        """
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)        
        #render form 
        item_form = Orden_trabajo_Ot_ItemFormSet(instance = self.object)
        
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
        
        item_form = Orden_trabajo_Ot_ItemFormSet(instance = Orden_trabajo())
        item_form = Orden_trabajo_Ot_ItemFormSet(request.POST,request.FILES,instance= self.object )
        
        if (form.is_valid() and item_form.is_valid()):

            
            self.object = form.save(commit=False)
            
            self.object.save()
            item_form.save()
            #Eliminar lo indicado del subnivel
            return HttpResponseRedirect(self.get_success_url())
            
        else:
            return self.form_invalid(form, item_form)
                
    def form_invalid(self, form, item_form):
        """
        Llamada si un formulario es inválido. Re-renders context data con el formulario
        cargado y los errores
        """
        return self.render_to_response(
                self.get_context_data(form=form,
                                      item_form = item_form))

class Ot_ItemListar(ListView):
    paginate_by = 10
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        query2 = self.request.GET.get('q2')
        
        #primero todos
        queryset = Ot_Item.objects.order_by('-orden_trabajo','numero')
        
        if not query2 is None: #filtro por muestreo propio
            if query2 == 'si':
                queryset = queryset.filter( muestreo_propio= True)    
            elif query2 == 'no':
                queryset = queryset.filter( muestreo_propio= False)    
            
                
            
        if not query is None: #filtro por nombes y descripciones
            queryset = queryset.filter( Q(numero__icontains=query)| 
                                           Q(orden_trabajo__referencia__icontains=query) | 
                                           Q(item__matriz__nombre_matriz__icontains=query) | 
                                           Q(estado__estado_actual__icontains=query))
        
        return queryset

    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(Ot_ItemListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        q2 = self.request.GET.get('q2')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query']  = q
        if q2: #si existe el valor, lo agrego/actualizo en el contexto
            q2 = q2.replace(" ","+")
            context['query2']  = q2
        return context    


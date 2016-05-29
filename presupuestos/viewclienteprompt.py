 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas



from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView
cliente_fields = ('empresa','contacto', 'funcion', 'domicilio','localidad', 'telefono_fijo', 'telefono_movil','email','cuit','nota')

from .models import Cliente

class ClientePrompt(ListView):
    model = Cliente
    #context_object_name = 'lista_de_clientes' #opcion a object_list
    template_name = 'presupuestos/cliente_prompt.html'
    paginate_by = 10
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Cliente.objects.all()
        else:
            return Cliente.objects.filter( Q(contacto__icontains=query) |
                                           Q(empresa__icontains=query) )
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(ClientePrompt, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context 
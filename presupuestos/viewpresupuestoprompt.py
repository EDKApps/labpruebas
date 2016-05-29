 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas



from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import ListView
presupuesto_fields = ('cliente','fecha_solicitud','fecha_vencimiento','descripcion','tipo','estado','observacion')

from .models import Presupuesto

class PresupuestoPrompt(ListView):
    model = Presupuesto
    #context_object_name = 'lista_de_clientes' #opcion a object_list
    template_name = 'presupuestos/presupuesto_prompt.html'
    paginate_by = 10
    
    #búsqueda
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is None:
            return Presupuesto.objects.filter(Q(estado__estado_actual='aprobado')).order_by('-referencia')
        else:
            return Presupuesto.objects.filter( Q(estado__estado_actual='aprobado') & (Q(cliente__empresa__icontains=query) | 
										  Q(cliente__contacto__icontains=query) |
										  Q(referencia__icontains=query) )).order_by('-referencia')

    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(PresupuestoPrompt, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context 
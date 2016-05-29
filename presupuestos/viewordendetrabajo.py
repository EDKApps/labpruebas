 # -- coding: utf-8 --
from django.shortcuts import render
from django.http import HttpResponse

from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

def OrdenDeTrabajoListar(request): #pasar a clase genérica
    context_dict = {}
    return render(request, 'presupuestos/ordendetrabajo_list.html', context_dict)
"""
cliente_fields = ('empresa','contacto_nombre','contacto_apellido',
			 'domicilio','telefono_fijo','telefono_movil',
			 'email','cuit','nota')

from .models import Cliente

def labinicio(request):
    context_dict = {}
    return render(request, 'presupuestos/index.html', context_dict) 

class ClienteListar(ListView):
    model = Cliente
    #context_object_name = 'lista_de_clientes' #opcion a object_list
    paginate_by = 10

class ClienteCrear(CreateView):
    model = Cliente
    success_url = reverse_lazy('presupuestos:cliente_listar')
    fields = cliente_fields

class ClienteDetalle(DetailView):
    model = Cliente
    fields = cliente_fields

class ClienteModificar(UpdateView):
    model = Cliente
    fields = cliente_fields
	
    def get_success_url(self):
        return reverse('presupuestos:cliente_detalle', kwargs={
            'pk': self.object.pk,
        })

class ClienteBorrar(DeleteView):
    model = Cliente
    success_url = reverse_lazy('presupuestos:cliente_listar')
    fields = cliente_fields
"""

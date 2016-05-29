 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q #para OR en consultas
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError

from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
import json
cliente_fields = ('empresa','contacto', 'funcion', 'domicilio','localidad', 'telefono_fijo', 'telefono_movil','email','cuit','nota')

from .models import Cliente
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def labinicio(request):
    context_dict = {}
    return render(request, 'presupuestos/index.html', context_dict)

class ClienteListar(ListView):
    model = Cliente
    #context_object_name = 'lista_de_clientes' #opcion a object_list
    paginate_by = 10

    @method_decorator(login_required)
    @method_decorator(permission_required("presupuestos.ver_cliente"))
    def dispatch(self, request, *args, **kwargs):
       return super(self.__class__, self).dispatch(request, *args, **kwargs)

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
        context = super(ClienteListar, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q: #si existe el valor, lo agrego/actualizo en el contexto
            q = q.replace(" ","+")
            context['query'] = q
        return context


class ClienteCrear(CreateView):
    model = Cliente
    fields = cliente_fields

    def get_success_url(self):
        return reverse('presupuestos:cliente_detalle', kwargs={
            'pk': self.object.pk,
        })

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

    def delete(self, request, *args, **kwargs):
        cliente = self.get_object()

        try:
            cliente.delete()
            estado = 'Cliente eliminada correctamente'
        except ValidationError as e:
            estado = 'Objeto protegido.' + str(e)
        respuesta = estado

        return render(request, 'presupuestos/confirmar_borrado.html',{"respuesta":respuesta })

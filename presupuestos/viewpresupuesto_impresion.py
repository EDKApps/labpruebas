 # -- coding: utf-8 --
from django import forms
from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.extras.widgets import SelectDateWidget
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.db.models import Q #para OR en consultas

from .models import Presupuesto

presupuesto_impresion_fields = ('impresion_introduccion', 'impresion_nota_muestreo', 'impresion_condiciones_comerciales', 'impresion_condiciones_tecnicas')

class Presupuesto_ImpresionModificar(UpdateView):
    model = Presupuesto
    fields = presupuesto_impresion_fields
    #form_class = PresupuestoFormModificar
    template_name = 'presupuestos/presupuesto_impresion_form.html'

    def get_success_url(self):
        return reverse_lazy('presupuestos:presupuesto_listar')


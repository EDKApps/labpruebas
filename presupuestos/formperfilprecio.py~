# -- coding: utf-8 --
from django import forms
from django.forms import ModelForm, BaseInlineFormSet
from django.forms.models import inlineformset_factory

from .models import PerfilPrecio, PerfilPrecio_Parametro, Parametro, Tecnica


class PerfilPrecioForm(ModelForm):
	class Meta:
		model = PerfilPrecio
		fields = ('nombre','matriz','precio','fecha_precio', 'fuente_precio')

class Perfil_Parametro_Form(BaseInlineFormSet):
	class Meta:
		model = PerfilPrecio_Parametro
		fields= '__all__'
		
	def add_fields(self, form, index):
		super(Perfil_Parametro_Form, self).add_fields(form, index)
		form.fields['parametro'] = forms.ModelChoiceField(
				queryset = Parametro.objects.order_by('nombre_par'))
		form.fields['tecnica'] = forms.ModelChoiceField(
				queryset = Tecnica.objects.order_by('nombre_tec'))	
	
#Modifico el form basico para incluir el orden en los combos dfd
class CustomInlineFormSet(ModelForm):
	
	#ordenar los combos
	def get_form(self, form_class):
		form = super(CustomInlineFormSet, self).get_form(form_class)
		print form.fields
		form.fields['parametro'] = forms.ModelChoiceField(queryset = Parametro.objects.order_by('nombre_par'))
		form.fields['tecnica'] = forms.ModelChoiceField(queryset = Tecnica.objects.order_by('nombre_tec'))
		return form		
	
PerfilPrecio_ParametroFormSet = inlineformset_factory(PerfilPrecio, PerfilPrecio_Parametro, fields='__all__',
													  formset = Perfil_Parametro_Form)

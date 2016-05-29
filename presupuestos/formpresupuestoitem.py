# -- coding: utf-8 --
from django import forms
from django.forms import ModelForm, BaseInlineFormSet
from django.forms.models import inlineformset_factory
from .models import Presupuesto, Item, Matriz

class PresupuestoForm(ModelForm):
	class Meta:
		model = Presupuesto
		fields = '__all__'

class Presupuesto_Item_Form(BaseInlineFormSet):
	class Meta:
		model = Item
		fields= '__all__'

	def add_fields(self, form, index):
		super(Presupuesto_Item_Form, self).add_fields(form, index)
		form.fields['matriz'] = forms.ModelChoiceField(
				queryset = Matriz.objects.order_by('nombre_matriz'))
	"""
	def save(self, commit=True):
		instance = super(Presupuesto_Item_Form, self).save(commit=False)
		if commit:
			instance.save()
		return instance
	"""

class CustomInlineFormSet(ModelForm):
	
	#ordenar los combos
	def get_form(self, form_class):
		form = super(CustomInlineFormSet, self).get_form(form_class)
		#print form.fields
		form.fields['matriz'] = forms.ModelChoiceField(queryset = Matriz.objects.order_by('nombre_matriz'))
		return form		

Presupuesto_ItemFormSet = inlineformset_factory(Presupuesto, Item, fields='__all__', formset = Presupuesto_Item_Form)
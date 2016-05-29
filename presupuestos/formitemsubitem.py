from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Item, Subitem_parametro, Subitem_perfil

#para que no figure field 'seleccionado'
item_fields = ('presupuesto', 'numero', 'descripcion', 'matriz', 'cantidadMuestra', 'descuento', 'total_sin_descuento', 'total_con_descuento')

class ItemForm(ModelForm):
	class Meta:
		model = Item
		fields = item_fields

class Subitem_parametro_Form(ModelForm):
	class Meta:
		model = Subitem_parametro
		fields= '__all__'

	def save(self, commit=True):
		instance = super(Subitem_parametro_Form, self).save(commit=False)
		if commit:
			instance.save()
		return instance 

class Subitem_perfil_Form(ModelForm):
	class Meta:
		model = Subitem_perfil
		fields= '__all__'

	def save(self, commit=True):
		instance = super(Subitem_parametro_Form, self).save(commit=False)
		if commit:
			instance.save()
		return instance 
	
Subitem_parametroFormSet = inlineformset_factory(Item, Subitem_parametro, fields='__all__', extra=0)
Subitem_perfilFormSet = inlineformset_factory(Item, Subitem_perfil, fields='__all__', extra=0)

from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Item, Subitem_parametro, Subitem_perfil

class ItemForm(ModelForm):
	class Meta:
		model = Item
		fields = '__all__'

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
	
Subitem_parametroFormSet = inlineformset_factory(Item, Subitem_parametro, fields='__all__')
Subitem_perfilFormSet = inlineformset_factory(Item, Subitem_perfil, fields='__all__')
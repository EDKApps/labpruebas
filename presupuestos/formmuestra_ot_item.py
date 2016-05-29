from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Muestra, Ot_Item


class Muestra_Ot_ItemForm(ModelForm):
	class Meta:
		model = Ot_Item
		fields= '__all__'

	def save(self, commit=True):
		instance = super(Muestra_Ot_ItemForm, self).save(commit=False)
		if commit:
			instance.save()
		return instance 

Muestra_Ot_ItemFormSet = inlineformset_factory(Ot_Item, Muestra, fields='__all__')

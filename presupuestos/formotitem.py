from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Orden_trabajo, Ot_Item

class Orden_trabajoForm(ModelForm):
	class Meta:
		model = Orden_trabajo
		fields = '__all__'

class Orden_trabajo_Ot_Item_Form(ModelForm):
	class Meta:
		model = Ot_Item
		fields= '__all__'

	def save(self, commit=True):
		instance = super(Orden_trabajo_Ot_Item_Form, self).save(commit=False)
		if commit:
			instance.save()
		return instance 

Orden_trabajo_Ot_ItemFormSet = inlineformset_factory(Orden_trabajo, Ot_Item, fields='__all__', extra=0)

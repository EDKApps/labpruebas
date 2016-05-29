from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Presupuesto, Campania

class PresupuestoForm(ModelForm):
	class Meta:
		model = Presupuesto
		fields = '__all__'

class Presupuesto_Campania_Form(ModelForm):
	class Meta:
		model = Campania
		fields= '__all__'

	def save(self, commit=True):
		instance = super(Presupuesto_Campania_Form, self).save(commit=False)
		if commit:
			instance.save()
		return instance 

Presupuesto_CampaniaFormSet = inlineformset_factory(Presupuesto, Campania, fields='__all__')

from django import forms

from django.forms.models import modelformset_factory

from .models import variation



class VariationInventoryForm(forms.ModelForm):
	class Meta:
		model=variation
		fields= [
			"title",
			"price",
			"sale_price",
			"inventory",
			"active",
		]

VariationInventoryFormSet = modelformset_factory(variation,form=VariationInventoryForm ,extra=1)
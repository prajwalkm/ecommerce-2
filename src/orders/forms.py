from django import forms
from django.contrib.auth import  get_user_model

from .models import UserAddress,Order

user=get_user_model()


class GuestCheckoutForm(forms.Form):
	email=forms.EmailField()
	email2=forms.EmailField(label='verify Email')


	def clean_email2(self):
		email=self.cleaned_data.get('email')
		email2=self.cleaned_data.get('email2')

		if email==email2:
			user_exists=user.objects.filter(email=email).count()
			if user_exists !=0:
				raise forms.ValidationError('This user  already exists .please login instead')
			return email2
		else:
			raise forms.ValidationError('please confirm emails are same')


class AddressForm(forms.Form):
	billing_address=forms.ModelChoiceField(
		queryset=UserAddress.objects.filter(type="billing"),
		widget=forms.RadioSelect,
		empty_label=None,
		)
	shipping_address=forms.ModelChoiceField(
		queryset=UserAddress.objects.filter(type="shipping"),
		widget=forms.RadioSelect,
		empty_label=None,

		)


class UserAddressForm(forms.ModelForm):
	class Meta:
		model=UserAddress
		fields=[
		'street',
		'city',
		'state',
		'zipcode',
		'type',
		'mobileNumber',

			]



class OrderForm(forms.ModelForm):
	class Meta:
		model=Order
		fields=['status']








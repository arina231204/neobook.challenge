from django import forms

class OrderForm(forms.Form):
    address = forms.CharField(max_length=255)
    name = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20)
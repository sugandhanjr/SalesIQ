from django import forms
from django.contrib.auth.models import User
from .models import Product, SalesData

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price']

class SalesDataForm(forms.ModelForm):
    class Meta:
        model = SalesData
        fields = ['product', 'quantity', 'sale_price', 'sale_date']
        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import PurchaseOrder, PurchaseRequest, Quotation
from django.contrib.auth.forms import  AuthenticationForm, UsernameField

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
        
class PurchaseRequestForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = ['product_name', 'quantity', 'description']

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['supplier_name', 'quotation_file', 'price']

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier_name', 'product_name', 'quantity', 'price', 'status']

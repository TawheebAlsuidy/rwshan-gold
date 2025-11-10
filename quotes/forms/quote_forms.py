from django import forms
from django.utils.translation import gettext_lazy as _
from quotes.models.quote_models import QuoteRequest
from products.models.product_models import Product, FabricOption, ColorOption


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = [
            'product', 'fabric', 'color', 'quantity', 'logo_complexity',
            'company_name', 'contact_person', 'email', 'phone', 'notes'
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'fabric': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'logo_complexity': forms.Select(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
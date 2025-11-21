from django import forms
from django.utils.translation import gettext_lazy as _
from configurator.models.configurator_models import UniformDesign, Product


class UniformDesignForm(forms.ModelForm):
    class Meta:
        model = UniformDesign
        fields = ['product', 'fabric', 'color',  'logo', 'notes']
        widgets = {
            'color': forms.TextInput(attrs={
                'type': 'color',
                'class': 'form-control form-control-color',
                'style': 'width: 80px; height: 40px;'
            }),
        }
     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially show all products or none until filtered by view
        self.fields['product'].queryset = Product.objects.none()
        
        # Make the product field required and improve its display
        self.fields['product'].widget.attrs.update({'class': 'form-select'})
        self.fields['fabric'].widget.attrs.update({'class': 'form-select'})
        self.fields['logo'].widget.attrs.update({
            'class': 'form-control',
            'disabled': 'disabled'
        })
        self.fields['notes'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'أدخل أي متطلبات أو ملاحظات خاصة...'
        })
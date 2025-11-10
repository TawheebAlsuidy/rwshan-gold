from django import forms
from django.utils.translation import gettext_lazy as _
from products.models.product_models import Product


class ProductFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label=_('Category')
    )
    min_price = forms.DecimalField(
        required=False,
        label=_('Min Price')
    )
    max_price = forms.DecimalField(
        required=False,
        label=_('Max Price')
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from products.models.product_models import ProductCategory
        self.fields['category'].queryset = ProductCategory.objects.all()
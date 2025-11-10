from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from products.models.product_models import ProductCategory, Product
from django.http import JsonResponse
def get_products_by_category(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
        products_data = [
            {
                'id': product.id,
                'name': product.safe_translation_getter('name', any_language=True)
            }
            for product in products
        ]
        return JsonResponse({'products': products_data})
    return JsonResponse({'products': []})


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'products/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = ProductCategory
    template_name = 'products/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'category_slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category=self.object)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'product_slug'
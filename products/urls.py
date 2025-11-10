from django.urls import path
from products.views import product_views as views

app_name = 'products'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:category_slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('api/products/', views.get_products_by_category, name='get_products_by_category'),
]
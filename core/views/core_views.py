from django.views.generic import TemplateView
from products.models.product_models import ProductCategory
from testimonials.models.testimonial_models import Testimonial, Client


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_categories'] = ProductCategory.objects.all()[:5]
        context['testimonials'] = Testimonial.objects.filter(is_featured=True)[:3]
        context['clients'] = Client.objects.all()
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
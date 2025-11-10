from django.views.generic import TemplateView, CreateView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from configurator.models.configurator_models import UniformDesign
from configurator.forms.configurator_forms import UniformDesignForm
from products.models.product_models import ProductCategory, Product, FabricOption, ColorOption
from configurator.utils import generate_uniform_preview

class ConfiguratorStartView(TemplateView):
    template_name = 'configurator/start.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context

class ConfiguratorStep1View(CreateView):
    model = UniformDesign
    form_class = UniformDesignForm
    template_name = 'configurator/step1.html'
    success_url = reverse_lazy('configurator:step2')
    
    def get_success_url(self):
        # تأكد من أن هذا الرابط صحيح ويؤدي إلى الصفحة التالية
        return reverse_lazy('configurator:step2')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Get category from URL parameters
        category_id = self.request.GET.get('category')
        if category_id:
            # Filter products by category
            form.fields['product'].queryset = Product.objects.filter(category_id=category_id)
        return form

    def get_initial(self):
        initial = super().get_initial()
        # Set initial category if provided in URL
        category_id = self.request.GET.get('category')
        if category_id:
            initial['category'] = category_id
        return initial

    def form_valid(self, form):
        # Save the design but don't commit to DB yet
        design = form.save(commit=False)
        if self.request.user.is_authenticated:
            design.user = self.request.user
        design.save()
        # Store the design ID in session for next steps
        self.request.session['current_design_id'] = design.id
        return super().form_valid(form)
    
    def get_success_url(self):
        # تأكد من أن هذا الرابط صحيح ويؤدي إلى الصفحة التالية
        return reverse_lazy('configurator:step2')

class ConfiguratorStep2View(TemplateView):
    template_name = 'configurator/step2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        design_id = self.request.session.get('current_design_id')
        if design_id:
            design = get_object_or_404(UniformDesign, id=design_id)

            # Try to generate preview if not already generated
            
            try:
                generate_uniform_preview(design)
            except Exception as e:
                print("Preview generation failed:", e)

            context['design'] = design
        return context


class ConfiguratorPreviewView(DetailView):
    model = UniformDesign
    template_name = 'configurator/preview.html'
    context_object_name = 'design'

    def get_object(self):
        design_id = self.request.session.get('current_design_id')
        return get_object_or_404(UniformDesign, id=design_id)
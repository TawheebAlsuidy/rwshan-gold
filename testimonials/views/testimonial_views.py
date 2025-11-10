from django.views.generic import ListView, DetailView
from django.db.models import Q
from testimonials.models.testimonial_models import Testimonial, ClientPartner, CaseStudy, Client


class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/list.html'
    context_object_name = 'testimonials'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Testimonial.objects.all()
        
        # Filter featured testimonials if requested
        featured = self.request.GET.get('featured')
        if featured:
            queryset = queryset.filter(is_featured=True)
            
        return queryset.prefetch_related('translations')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_testimonials'] = Testimonial.objects.filter(is_featured=True)[:6]
        return context


class ClientListView(ListView):
    model = Client
    template_name = 'testimonials/list.html'
    context_object_name = 'clients'
    paginate_by = 12
    
    def get_queryset(self):
        return Client.objects.all()
    
class CaseStudyListView(ListView):
    model = CaseStudy
    template_name = 'testimonials/case_studies.html'
    context_object_name = 'case_studies'
    paginate_by = 6
    
    def get_queryset(self):
        return CaseStudy.objects.all().select_related('client').prefetch_related('translations')


class CaseStudyDetailView(DetailView):
    model = CaseStudy
    template_name = 'testimonials/case_study_detail.html'
    context_object_name = 'case_study'
    slug_url_kwarg = 'case_study_slug'
    
    def get_queryset(self):
        return CaseStudy.objects.select_related('client').prefetch_related('translations')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related case studies (same client)
        context['related_case_studies'] = CaseStudy.objects.filter(
            client=self.object.client
        ).exclude(pk=self.object.pk)[:3]
        return context
from django.urls import path
from testimonials.views import testimonial_views as views

app_name = 'testimonials'

urlpatterns = [
    path('', views.ClientListView.as_view(), name='list'),
    # path('clients/', views.TestimonialListView.as_view(), name='clients'),
    path('case-studies/', views.CaseStudyListView.as_view(), name='case_studies'),
    path('case-study/<slug:case_study_slug>/', views.CaseStudyDetailView.as_view(), name='case_study_detail'),
]
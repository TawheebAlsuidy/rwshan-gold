from django.urls import path
from contact.views import contact_views as views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
    path('success/', views.ContactSuccessView.as_view(), name='success'),
    path('faq/', views.FAQListView.as_view(), name='faq'),
]
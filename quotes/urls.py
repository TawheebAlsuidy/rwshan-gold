from django.urls import path
from quotes.views import quote_views as views

app_name = 'quotes'

urlpatterns = [
    path('calculator/', views.QuoteCalculatorView.as_view(), name='calculator'),
    path('request/', views.QuoteRequestCreateView.as_view(), name='request_create'),
    path('success/', views.QuoteSuccessView.as_view(), name='success'),
    path('list/', views.QuoteListView.as_view(), name='list'),
    path('detail/<int:pk>/', views.QuoteDetailView.as_view(), name='detail'),
]
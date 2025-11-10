from django.urls import path
from configurator.views import configurator_views

app_name = 'configurator'

urlpatterns = [
    path('', configurator_views.ConfiguratorStartView.as_view(), name='start'),
    path('step1/', configurator_views.ConfiguratorStep1View.as_view(), name='step1'),
    path('step2/', configurator_views.ConfiguratorStep2View.as_view(), name='step2'),
    path('preview/', configurator_views.ConfiguratorPreviewView.as_view(), name='preview'),
]
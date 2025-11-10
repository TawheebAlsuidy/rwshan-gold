from django.urls import path
from blog.views import blog_views as views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('category/<slug:category_slug>/', views.CategoryPostListView.as_view(), name='category_list'),
    path('<slug:post_slug>/', views.PostDetailView.as_view(), name='detail'),
]
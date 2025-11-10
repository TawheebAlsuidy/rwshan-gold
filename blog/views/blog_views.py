from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from blog.models.blog_models import Post, PostCategory


class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PostCategory.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_queryset(self):
        return Post.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related posts
        context['related_posts'] = Post.objects.filter(
            category=self.object.category,
            status='published'
        ).exclude(id=self.object.id)[:3]
        return context


class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/category_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        self.category = get_object_or_404(PostCategory, slug=self.kwargs['category_slug'])
        return Post.objects.filter(category=self.category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = PostCategory.objects.all()
        return context
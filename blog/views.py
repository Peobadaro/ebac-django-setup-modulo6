from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Category, Post


class PostListView(ListView):
    """Página inicial: lista os posts publicados."""

    queryset = Post.published.select_related("author", "category")
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 5


class CategoryPostListView(PostListView):
    """Posts publicados de uma categoria."""

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class PostDetailView(DetailView):
    """Página de um post publicado."""

    queryset = Post.published.select_related("author", "category")
    template_name = "blog/post_detail.html"
    context_object_name = "post"

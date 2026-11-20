from django.urls import path
from django.views.generic import DetailView

from .models import Post

app_name = "blog"

urlpatterns = [
    path("<slug:slug>/", DetailView.as_view(queryset=Post.published.all()), name="post_detail"),
]

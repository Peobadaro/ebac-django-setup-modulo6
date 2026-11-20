from django.db.models import Count, Q

from .models import Category, Post


def sidebar(request):
    """Dados da sidebar, disponíveis em todos os templates."""
    return {
        "sidebar_categories": Category.objects.annotate(
            total=Count("posts", filter=Q(posts__status=Post.Status.PUBLISHED))
        ).filter(total__gt=0),
        "sidebar_recent_posts": Post.published.all()[:5],
    }

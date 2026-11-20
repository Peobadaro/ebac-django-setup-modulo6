import pytest
from django.urls import reverse

from blog.models import Post

from .factories import CategoryFactory, PostFactory

pytestmark = pytest.mark.django_db


def publicado(**kwargs):
    return PostFactory(status=Post.Status.PUBLISHED, **kwargs)


class TestIndex:
    def test_usa_os_templates_base_index_e_sidebar(self, client):
        response = client.get(reverse("blog:index"))
        assert response.status_code == 200
        templates = [t.name for t in response.templates]
        assert "blog/index.html" in templates
        assert "base.html" in templates
        assert "includes/sidebar.html" in templates

    def test_mostra_so_posts_publicados(self, client):
        publicado(title="Post publicado")
        PostFactory(title="Post rascunho")
        content = client.get(reverse("blog:index")).content.decode()
        assert "Post publicado" in content
        assert "Post rascunho" not in content

    def test_paginacao_de_5_posts(self, client):
        for _ in range(7):
            publicado()
        response = client.get(reverse("blog:index"))
        assert len(response.context["posts"]) == 5
        assert response.context["is_paginated"]

    def test_mensagem_quando_nao_ha_posts(self, client):
        assert "Nenhum post publicado ainda." in client.get(reverse("blog:index")).content.decode()


class TestPostDetail:
    def test_mostra_o_post(self, client):
        post = publicado(title="Detalhe do post", content="Texto completo do post")
        response = client.get(post.get_absolute_url())
        assert response.status_code == 200
        assert "blog/post_detail.html" in [t.name for t in response.templates]
        assert "Texto completo do post" in response.content.decode()

    def test_rascunho_retorna_404(self, client):
        post = PostFactory()
        assert client.get(post.get_absolute_url()).status_code == 404


class TestCategoria:
    def test_filtra_posts_da_categoria(self, client):
        python = CategoryFactory(name="Python")
        publicado(title="Post de Python", category=python)
        publicado(title="Post de outra categoria")
        response = client.get(reverse("blog:category", args=[python.slug]))
        assert [p.title for p in response.context["posts"]] == ["Post de Python"]
        assert "Categoria: Python" in response.content.decode()

    def test_categoria_inexistente_retorna_404(self, client):
        assert client.get(reverse("blog:category", args=["nao-existe"])).status_code == 404


class TestSidebar:
    def test_lista_categorias_com_posts_e_recentes(self, client):
        python = CategoryFactory(name="Python")
        CategoryFactory(name="Sem posts")
        publicado(title="Recente", category=python)
        response = client.get(reverse("blog:index"))
        nomes = [c.name for c in response.context["sidebar_categories"]]
        assert nomes == ["Python"]
        assert [p.title for p in response.context["sidebar_recent_posts"]] == ["Recente"]

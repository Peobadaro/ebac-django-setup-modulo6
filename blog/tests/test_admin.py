import pytest
from django.contrib.admin.sites import site
from django.urls import reverse

from blog.models import Category, Post

from .factories import PostFactory

pytestmark = pytest.mark.django_db


def test_post_e_category_registrados_no_admin():
    assert Post in site._registry
    assert Category in site._registry


def test_listagem_de_posts_abre(admin_client):
    PostFactory.create_batch(3)
    response = admin_client.get(reverse("admin:blog_post_changelist"))
    assert response.status_code == 200
    assert response.context["cl"].result_count == 3


def test_busca_por_titulo(admin_client):
    PostFactory(title="Aprendendo Django Admin")
    PostFactory(title="Outro assunto")
    response = admin_client.get(reverse("admin:blog_post_changelist"), {"q": "Admin"})
    assert response.context["cl"].result_count == 1


def test_filtro_por_status(admin_client):
    PostFactory(status=Post.Status.PUBLISHED)
    PostFactory()
    response = admin_client.get(reverse("admin:blog_post_changelist"), {"status__exact": "draft"})
    assert response.context["cl"].result_count == 1


def test_formulario_de_novo_post_abre(admin_client):
    response = admin_client.get(reverse("admin:blog_post_add"))
    assert response.status_code == 200


def test_acao_publicar(admin_client):
    posts = PostFactory.create_batch(2)
    admin_client.post(
        reverse("admin:blog_post_changelist"),
        {"action": "publicar", "_selected_action": [p.pk for p in posts]},
    )
    assert Post.published.count() == 2
    assert not Post.objects.filter(published_at__isnull=True).exists()


def test_acao_voltar_para_rascunho(admin_client):
    post = PostFactory(status=Post.Status.PUBLISHED)
    admin_client.post(
        reverse("admin:blog_post_changelist"),
        {"action": "voltar_para_rascunho", "_selected_action": [post.pk]},
    )
    post.refresh_from_db()
    assert post.status == Post.Status.DRAFT


def test_usuario_comum_nao_acessa_o_admin(client, django_user_model):
    user = django_user_model.objects.create_user("comum", password="senha-teste-123")
    client.force_login(user)
    response = client.get(reverse("admin:blog_post_changelist"))
    assert response.status_code == 302

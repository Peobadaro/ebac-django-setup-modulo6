import pytest
from django.db import IntegrityError

from blog.models import Category, Post

from .factories import CategoryFactory, PostFactory, UserFactory

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------- Category

class TestCategory:
    def test_str_retorna_o_nome(self):
        category = CategoryFactory(name="Python")
        assert str(category) == "Python"

    def test_slug_gerado_automaticamente(self):
        category = CategoryFactory(name="Django Avançado")
        assert category.slug == "django-avancado"

    def test_nome_deve_ser_unico(self):
        CategoryFactory(name="Python")
        with pytest.raises(IntegrityError):
            CategoryFactory(name="Python")

    def test_ordenacao_por_nome(self):
        CategoryFactory(name="Zeta")
        CategoryFactory(name="Alfa")
        assert [c.name for c in Category.objects.all()] == ["Alfa", "Zeta"]


# -------------------------------------------------------------------- Post

class TestPost:
    def test_str_retorna_o_titulo(self):
        post = PostFactory(title="Primeiro post")
        assert str(post) == "Primeiro post"

    def test_slug_gerado_a_partir_do_titulo(self):
        post = PostFactory(title="Olá Mundo com Django")
        assert post.slug == "ola-mundo-com-django"

    def test_status_padrao_e_rascunho(self):
        post = PostFactory()
        assert post.status == Post.Status.DRAFT
        assert post.published_at is None

    def test_publicar_preenche_data_de_publicacao(self):
        post = PostFactory(status=Post.Status.PUBLISHED)
        assert post.published_at is not None

    def test_manager_published_retorna_so_publicados(self):
        PostFactory(status=Post.Status.DRAFT)
        publicado = PostFactory(status=Post.Status.PUBLISHED)
        assert list(Post.published.all()) == [publicado]
        assert Post.objects.count() == 2

    def test_slug_deve_ser_unico(self):
        PostFactory(title="Mesmo título")
        with pytest.raises(IntegrityError):
            PostFactory(title="Mesmo título")

    def test_get_absolute_url(self):
        post = PostFactory(title="Meu post")
        assert post.get_absolute_url() == "/meu-post/"


# -------------------------------------------------------- Relacionamentos

class TestRelacionamentos:
    def test_autor_tem_varios_posts(self):
        autor = UserFactory()
        PostFactory.create_batch(3, author=autor)
        assert autor.posts.count() == 3

    def test_categoria_tem_varios_posts(self):
        category = CategoryFactory()
        PostFactory.create_batch(2, category=category)
        assert category.posts.count() == 2

    def test_apagar_categoria_mantem_o_post(self):
        post = PostFactory()
        post.category.delete()
        post.refresh_from_db()
        assert post.category is None

    def test_apagar_autor_apaga_os_posts(self):
        post = PostFactory()
        post.author.delete()
        assert not Post.objects.filter(pk=post.pk).exists()

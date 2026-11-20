import factory
from django.contrib.auth import get_user_model

from blog.models import Category, Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]

    username = factory.Sequence(lambda n: f"usuario{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@email.com")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Categoria {n}")


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f"Meu post número {n}")
    summary = factory.Faker("sentence", locale="pt_BR")
    content = factory.Faker("paragraph", locale="pt_BR")
    author = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)

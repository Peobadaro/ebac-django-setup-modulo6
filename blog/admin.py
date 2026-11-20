from django.contrib import admin, messages
from django.utils import timezone

from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "total_posts", "created_at"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}

    @admin.display(description="posts")
    def total_posts(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Listagem
    list_display = ["title", "author", "category", "status", "published_at", "updated_at"]
    list_display_links = ["title"]
    list_editable = ["status"]
    list_filter = ["status", "category", "author", "created_at"]
    search_fields = ["title", "summary", "content"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    list_per_page = 20
    list_select_related = ["author", "category"]

    # Formulário
    prepopulated_fields = {"slug": ["title"]}
    autocomplete_fields = ["category"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = [
        ("Conteúdo", {"fields": ["title", "slug", "summary", "content"]}),
        ("Classificação", {"fields": ["author", "category"]}),
        ("Publicação", {"fields": ["status", "published_at"]}),
        ("Datas", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    # Ações em massa
    actions = ["publicar", "voltar_para_rascunho"]

    @admin.action(description="Publicar posts selecionados")
    def publicar(self, request, queryset):
        total = queryset.filter(published_at__isnull=True).update(published_at=timezone.now())
        updated = queryset.update(status=Post.Status.PUBLISHED)
        self.message_user(request, f"{updated} post(s) publicado(s).", messages.SUCCESS)
        return total

    @admin.action(description="Voltar posts selecionados para rascunho")
    def voltar_para_rascunho(self, request, queryset):
        updated = queryset.update(status=Post.Status.DRAFT)
        self.message_user(request, f"{updated} post(s) voltaram para rascunho.", messages.SUCCESS)

    def get_changeform_initial_data(self, request):
        # Novo post já vem com o usuário logado como autor
        return {"author": request.user.pk}

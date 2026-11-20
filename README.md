# EBAC – Projeto Django (portfólio)

Projeto Django criado no curso **Profissão: Desenvolvedor Full Stack Python** da EBAC.

Autor: **Pedro Badaró Ferreira** ([@Peobadaro](https://github.com/Peobadaro))

## Como rodar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abra http://127.0.0.1:8000/ no navegador.

## App `blog` (Módulo 7)

- **Modelos:** `Category` e `Post` (Post → User e Post → Category, ambos 1:N)
- **Post:** título, slug automático, resumo, conteúdo, status (rascunho/publicado), datas e manager `Post.published`
- **Testes:** `pytest` + `pytest-django` + `factory_boy` em `blog/tests/`

```bash
pip install -r requirements-dev.txt
pytest
```

## Templates (Módulo 9)

| Template | Função |
|---|---|
| `templates/base.html` | Layout base: cabeçalho, bloco de conteúdo, sidebar e rodapé, com CSS em `static/css/style.css` |
| `templates/includes/sidebar.html` | Sidebar com "Sobre", categorias e posts recentes (dados do context processor `blog.context_processors.sidebar`) |
| `blog/templates/blog/index.html` | Página inicial com os posts publicados e paginação (também usada na página de categoria) |
| `blog/templates/blog/post_detail.html` | Página de um post |
| `blog/templates/blog/_post_card.html` | Card de post reutilizado na listagem |

Rotas: `/` (posts), `/categoria/<slug>/` e `/<slug-do-post>/`.

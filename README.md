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

## Django Admin (Módulo 10)

```bash
python manage.py createsuperuser
python manage.py runserver
```

Acesse http://127.0.0.1:8000/admin/ → **Blog › Posts**: listagem com filtros (status, categoria, autor, data), busca, status editável na lista e ações em massa para publicar ou voltar para rascunho.

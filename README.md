# MOL Ticket System

Sistema de Gestão de Tickets (Chamados) desenvolvido com Django + Django REST Framework.

## Instalação local
```bash
git clone git@github.com:carlos-e-mattos/mol-ticket-system.git
cd mol-ticket-system

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Com Docker
```bash
docker-compose up --build
```

Após subir, crie o superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

## URLs principais

| URL | Descrição |
|-----|-----------|
| `/tickets/` | Listagem de tickets |
| `/tickets/novo/` | Criar ticket |
| `/tickets/<id>/` | Detalhe do ticket |
| `/tickets/<id>/editar/` | Editar ticket |
| `/tickets/<id>/excluir/` | Excluir ticket |
| `/admin/` | Django Admin |
| `/api/` | API REST (DRF) |
| `/api/tickets/` | Endpoint tickets |
| `/api/clientes/` | Endpoint clientes |
| `/login/` | Login |

## Testes
```bash
python manage.py test tickets
```

## Lint
```bash
ruff check .
```
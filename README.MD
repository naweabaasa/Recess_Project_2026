# BreadWise Backend

This is the Flask backend for the BreadWise application. The project uses an application factory pattern and registers all API blueprints in `app/__init__.py`.

## Project structure

- `app/__init__.py` — creates the Flask app and registers blueprints
- `app/controllers/` — API route handlers
- `app/models/` — database models
- `app/extensions.py` — Flask extensions setup
- `config.py` — application configuration and environment variables
- `run.py` — app entry point
- `migrations/` — Alembic migration files

## Tech stack

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-JWT-Extended
- Flask-CORS
- Flask-Bcrypt
- MySQL (configured through environment variables or local defaults)

## Application factory

The app is created with `create_app()` in `app/__init__.py`, and all blueprints are registered from `app/controllers/__init__.py`.

Registered blueprints include:

- `auth_bp` → `/api/auth`
- `admin_bp` → `/api/admins`
- `category_bp` → `/api/categories`
- `product_bp` → `/api/products`
- `order_bp` → `/api/orders`
- `delivery_bp` → `/api/deliveries`
- `public_bp` → `/api/public`
- `page_content_bp` → `/api/pages`
- `upload_bp` → `/api/upload`

## Configuration

The app reads configuration values from environment variables in `config.py`.

Default values:

- `DB_USER` = `root`
- `DB_PASSWORD` = empty string
- `DB_HOST` = `localhost`
- `DB_NAME` = `bread_wise_db`
- `SECRET_KEY` = generated random key if not set
- `JWT_SECRET_KEY` = generated random key if not set

The database URL is built as:

```python
mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}
```

## Running the app

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
python run.py
```

Or with Flask directly:

```bash
flask run
```

## Authentication

Login endpoint:

```http
POST /api/auth/login
```

Request body:

```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "admin": {
    "id": 1,
    "email": "admin@example.com",
    "name": "Admin Name"
  },
  "access_token": "<jwt_token>"
}
```

The JWT includes permissions such as:

- `manage_categories`
- `manage_products`
- `manage_orders`
- `manage_deliveries`
- `manage_page_content`
- `manage_admins`

## API overview

### Auth
- `POST /api/auth/login`

### Admins
- `GET /api/admins`
- `POST /api/admins`
- `PUT /api/admins/<admin_id>`
- `DELETE /api/admins/<admin_id>`

### Categories
- `GET /api/categories`
- `POST /api/categories`
- `PUT /api/categories/<category_id>`
- `DELETE /api/categories/<category_id>`

### Products
- `GET /api/products`
- `POST /api/products`
- `PUT /api/products/<product_id>`
- `DELETE /api/products/<product_id>`

### Orders
- `POST /api/orders`
- `GET /api/orders`
- `PUT /api/orders/<order_id>/status`

### Deliveries
- `GET /api/deliveries`
- `POST /api/deliveries`
- `PUT /api/deliveries/<delivery_id>`

### Page content
- `GET /api/pages` — fetch all page content grouped by page name
- `GET /api/pages/<page_name>` — fetch content for one page
- `PUT /api/pages/<page_name>` — update content blocks for one page

Example response for `GET /api/pages`:

```json
{
  "home": {
    "hero_title": "Welcome to BreadWise",
    "hero_subtitle": "Freshly baked every day"
  },
  "about": {
    "mission_statement": "We bring quality bread to our community"
  }
}
```

### Public routes
- `GET /api/public/categories`
- `GET /api/public/products`
- `GET /api/public/products/<product_id>`
- `GET /api/public/pages`
- `GET /api/public/pages/<page_name>`

### Upload
- `POST /api/upload/product-image`

## Notes

- The project uses JWT protection on admin routes via `permission_required` decorators.
- `page_content` stores content blocks with fields like `page_name`, `section_key`, and `content`.
- The application uses MySQL by default, but the testing config can use SQLite.

## Database migration

Migrations are managed with Flask-Migrate in the `migrations/` folder.

```bash
flask db migrate
flask db upgrade
```

This README reflects the actual code in this repository and not the older migration-only draft.

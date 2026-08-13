# BreadWise Backend

This is the backend API for the BreadWise Bakery application. It is built with Flask (Python) and uses a MySQL database to manage products, categories, orders, deliveries, and admin authentication.

## Technologies Used
- **Flask**: Web framework for Python.
- **Flask-SQLAlchemy**: ORM for database interactions.
- **Flask-Migrate**: Handles database migrations using Alembic.
- **Flask-JWT-Extended**: Manages JWT-based authentication for the admin panel.
- **Flask-Bcrypt**: Hashes passwords for secure storage.
- **Flask-Cors**: Handles Cross-Origin Resource Sharing for communicating with the React frontend.
- **PyMySQL**: MySQL driver for Python.

## Prerequisites
- Python 3.8+
- MySQL Server

## Setup Instructions

### 1. Clone the repository
Navigate to the `backend` directory of the project.

### 2. Create and Activate a Virtual Environment
**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root of the `backend` directory (you can copy `.env.example`). 
Example `.env` configuration:
```ini
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database Configuration
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_NAME=bread_wise_db
```

### 5. Database Setup
Make sure your MySQL server is running and create the database if it doesn't exist:
```sql
CREATE DATABASE bread_wise_db;
```

Run database migrations to create the tables:
```bash
flask db upgrade
```

*Note: If migrations are not initialized, you may need to run `flask db init` and `flask db migrate` first.*

### 6. Seed the Database
To populate the database with initial data (like the default admin user and page content), run the seed script:
```bash
python seed.py
```

### 7. Run the Application
Start the Flask development server:
```bash
python run.py
```
The server will start on `http://127.0.0.1:5000`.

## API Structure (Blueprints)
The backend is organized into several modular blueprints located in `app/controllers/`:
- **Auth (`/api/auth`)**: Admin login and token generation.
- **Admin (`/api/admins`)**: Manage admin users.
- **Categories (`/api/categories`)**: Manage product categories.
- **Products (`/api/products`)**: Manage products.
- **Orders (`/api/orders`)**: Manage customer orders.
- **Deliveries (`/api/deliveries`)**: Manage order deliveries.
- **Public (`/api/public`)**: Public endpoints for the frontend (products, categories, page content).
- **Pages (`/api/pages`)**: Admin endpoints for CMS page content.
- **Upload (`/api/upload`)**: Handles image uploads (product images, hero images) and saves them to the frontend's `public/images/` directory.

## Database Migration Order

To ensure correct foreign key relationships, the database tables should ideally be created in the following order:

**Layer 0: Independent Tables (No Foreign Keys)**
1. `admins`
2. `categories`
3. `page_content`

**Layer 1: Tables Referencing Layer 0**
4. `products` (depends on `categories`)
5. `orders`

**Layer 2: Tables Referencing Layer 1**
6. `deliveries` (depends on `orders`)

# --- README.md content ---
readme_content = """
# Multi-Tenant Book Management System

A production-grade FastAPI system for managing books with **multi-tenancy** (each organization has separate users/books) and robust **role-based access control** (Admin, Librarian, Member). Powered by Python 3.13+, PostgreSQL, FastAPI, SQLAlchemy, and Pydantic V2.

## 🚀 Features
- Multi-tenant data isolation: each tenant (organization/company) has private data
- JWT (access & refresh tokens) authentication
- Role-based permissions: Admin, Librarian, Member
- Secure password hashing (bcrypt)
- All CRUD operations for books and users
- PostgreSQL as the backend database (can use SQLite for local dev)
- Alembic migrations ready
- Fully async FastAPI API with OpenAPI/Swagger docs
- 100% Python 3.13+, SQLAlchemy 2.x, and Pydantic V2 compatible

## 🛠️ Tech Stack
- **Backend**: FastAPI `0.115.5`, Pydantic `2.10.3`
- **DB/ORM**: PostgreSQL 14+, SQLAlchemy `2.0.36`, Alembic `1.13.3`
- **Auth**: JWT (`python-jose`), passlib (bcrypt)
- **Testing**: `pytest`, `httpx`, `pytest-asyncio`
- **Other**: ORJSON (faster JSON responses), `python-multipart` (uploads), container-ready

## 📁 Project Structure
book-management-system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── auth/
│   └── utils/
├── requirements.txt
├── .env
├── .gitignore
└── README.md

## ⚡ Quick Start
1. Clone and Install  
   git clone <your-repo-url>  
   cd book-management-system  
   python3.13 -m venv venv  
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate  
   pip install -r requirements.txt

2. Configure Database (PostgreSQL)  
   CREATE DATABASE bookdb;  
   CREATE USER bookuser WITH PASSWORD 'securepassword';  
   GRANT ALL PRIVILEGES ON DATABASE bookdb TO bookuser;

   Edit `.env`:
   DATABASE_URL=postgresql://bookuser:securepassword@localhost/bookdb  
   SECRET_KEY=your-very-secret-key-min-32-chars

3. Run the App  
   uvicorn app.main:app --reload  
   # API docs: http://localhost:8000/api/docs

## ✨ Usage Examples
### Register a Tenant
curl -X POST http://localhost:8000/api/tenants/register -H "Content-Type: application/json" -d '{"name": "Acme Library", "subdomain": "acme"}'

### Login
curl -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d '{"username": "admin", "password": "ChangeMe123!", "tenant_subdomain": "acme"}'

### Add a Book
curl -X POST http://localhost:8000/api/books -H "Authorization: Bearer <ACCESS_TOKEN>" -H "Content-Type: application/json" -d '{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "isbn": "9780743273565", "quantity": 5}'

## 🔑 Role Permissions

| Role      | Books Read | Books Create | Books Update | Books Delete | Users Manage |
|-----------|------------|--------------|--------------|--------------|--------------|
| Member    | ✅         | ❌           | ❌           | ❌           | ❌           |
| Librarian | ✅         | ✅           | ✅           | ❌           | ❌           |
| Admin     | ✅         | ✅           | ✅           | ✅           | ✅           |

**All organizations are fully isolated at the data layer.**

## 🧪 Testing
pytest

## 📄 License
MIT License

## 🙏 Attribution
Inspired by best practices from the FastAPI ecosystem, Tiangolo, and the open Python community.
"""

# --- LOCAL_DB_SETUP.md content ---
local_db_content = """
Using a Local Database (SQLite) for Development

This project fully supports running with a local file-based SQLite database for development, demo, or small-scale usage—no need for PostgreSQL or any external server.

1. Configure .env for SQLite
In your project root, open .env and set:

DATABASE_URL=sqlite:///./bookdb.sqlite  
DATABASE_ECHO=False        # True for verbose SQL logging, False for normal use  
SECRET_KEY=put-your-strong-secret-key-here  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30  
REFRESH_TOKEN_EXPIRE_DAYS=7  
BASE_DOMAIN=localhost  
TENANT_URL_PATTERN=subdomain  
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

This creates a file named bookdb.sqlite in your project directory.

No setup or database server needed for SQLite.

2. Install Requirements

pip install -r requirements.txt

You don’t need psycopg2-binary for SQLite—keep it in requirements for easy switching back to PostgreSQL later.

3. Run the Application

uvicorn app.main:app --reload

App is now running with a local SQLite database.

All tables will be auto-created in bookdb.sqlite upon first run.

Visit http://localhost:8000/api/docs for interactive API docs.

4. Quick Test of Local Database

Register a tenant (org) via Swagger UI or:

curl -X POST http://localhost:8000/api/tenants/register \  
  -H "Content-Type: application/json" \  
  -d '{"name": "Local Demo Org", "subdomain": "demo"}'

Proceed with user signup, login, and CRUD as usual.

5. Switching Back to PostgreSQL (Production-Grade)

To deploy in production:

Change .env to:

DATABASE_URL=postgresql://bookuser:securepassword@localhost/bookdb

(Re-)create the database/user in PostgreSQL as described above.

6. Testing Data Isolation & RBAC (with SQLite)

Your test suite works with both SQLite and PostgreSQL.

Multi-tenant separation and role-based access are enforced in all supported database backends.

Sample pytest snippet:

def test_cross_tenant_data(client, token_a, token_b):
    # Org A creates a book
    client.post("/api/books", headers={"Authorization": f"Bearer {token_a}"}, json={...})
    # Org B cannot see Org A's book
    resp = client.get("/api/books/1", headers={"Authorization": f"Bearer {token_b}"})
    assert resp.status_code == 404

Summary

SQLite is ideal for development/Demo—no extra database infra needed.

To move to production or enable real concurrency, switch .env and DB to PostgreSQL.

All app logic (multi-tenancy, RBAC, isolation) is fully compatible with SQLite.

Add this section to your README to clarify usage for both local testing/development and production environments!
"""

# --- Write files ---
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

with open("LOCAL_DB_SETUP.md", "w", encoding="utf-8") as f:
    f.write(local_db_content)

print("README.md and LOCAL_DB_SETUP.md created successfully! 🎉")
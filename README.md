
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


## JWT Secret Key Generation
To securely sign your JWT tokens, you'll need a strong secret key. Follow these steps to generate one:

Step-by-step guide:
1. Open your terminal or Python environment.

2. Run the following Python code:
-> import secrets
-> print(secrets.token_urlsafe(48))

3. Copy the output, which will be a long, random, URL-safe string, e.g.
hHjA3vmQCLLIn5X_TzKGj2R6aWQGb9LHqeGDRPhXYYDUrzd-L3FI9QyOosE0MsRo

4.Update your .env file with this key:
SECRET_KEY=hHjA3vmQCLLIn5X_TzKGj2R6aWQGb9LHqeGDRPhXYYDUrzd-L3FI9QyOosE0MsRo

## Important notes:
Keep your secret key confidential.
Do not commit it to version control.
Always generate a new key for production environment.


Run the following Python code:
## ⚡ Quick Start
1. Clone and Install  
   git clone <your-repo-url>  
   cd book-management-system  
   python3.13 -m venv venv   # On Windows: python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate  
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

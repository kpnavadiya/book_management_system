
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

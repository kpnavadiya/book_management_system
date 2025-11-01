# Project API Endpoints and Descriptions

| URL Path                  | Description                                                            |
|---------------------------|------------------------------------------------------------------------|
| `/api/tenants/register`   | Register a new tenant (organization) — public signup endpoint          |
| `/api/auth/login`         | User login — returns JWT access and refresh tokens                     |
| `/api/auth/refresh`       | Refresh JWT access token using refresh token                           |
| `/api/auth/change-password` | Change password for authenticated user                               |
| `/api/users`              | Create/list users for current tenant (admin access needed)             |
| `/api/users/{user_id}`    | Get/update/delete a specific user under current tenant                 |
| `/api/books`              | Create/list books belonging to current tenant                          |
| `/api/books/{book_id}`    | Get/update/delete a specific book                                      |
| `/api/tenants/me`         | Get current user's tenant (organization) details                       |
| `/api/tenants/me` (PUT)   | Update current tenant info (admin only)                                |
| `/health`                 | Health check endpoint — returns server health status                   |
| `/`                       | Root endpoint — welcome message or API info                            |
| `/api/docs`               | Interactive Swagger UI for API documentation and testing               |
| `/api/openapi.json`       | OpenAPI JSON schema for API structure                                  |
| `/api/redoc`              | Alternative ReDoc API documentation UI                                |

---

## Notes

- All `/api/...` endpoints are under the configured API prefix (default `/api`).
- Most endpoints require JWT bearer tokens except those explicitly public (tenant register, login, docs, health).
- Admin roles required for sensitive operations like user and tenant management.
- Use `/api/docs` to explore and interact with the full API documentation.


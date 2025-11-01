# API Testing Guide Using Swagger UI

This guide will help you systematically test your FastAPI application’s endpoints using the interactive Swagger UI.

---

## Step 1: Open Swagger UI

- Open your web browser.
- Navigate to:

http://localhost:8000/api/docs

text

(Replace with your host and port if different.)

---

## Step 2: Register a Tenant (Organization)

- In the **Tenants** section, locate **POST /api/tenants/register**.
- Click to expand the endpoint.
- Click **Try it out**.
- Fill the JSON input like:

{
"name": "Acme Library",
"subdomain": "acme"
}

text

- Click **Execute**.
- Verify that you receive a **201 Created** status with tenant information.
- Note the `subdomain` (e.g., "acme") for future steps.

---

## Step 3: Login as Admin User

- In the **Auth** section, expand **POST /api/auth/login**.
- Click **Try it out**.
- Provide login credentials JSON:

{
"username": "admin",
"password": "ChangeMe123!",
"tenant_subdomain": "acme"
}

text

- Click **Execute**.
- Copy the returned `access_token` from the response for authorizing further requests.

---

## Step 4: Authorize Swagger UI For Secured APIs

- Click the **Authorize** button at the top-right corner.
- In the modal, enter your token as:

Bearer <access_token>

text

Replace `<access_token>` with the actual token.
- Click **Authorize**, then **Close** the modal.

---

## Step 5: Create a Book

- Expand **POST /api/books** in the **Books** section.
- Click **Try it out**.
- Fill the body with book details, e.g.,

{
"title": "1984",
"author": "George Orwell",
"isbn": "1234567890123",
"quantity": 10
}

text

- Click **Execute**.
- Confirm that the book is added successfully with a 200 or 201 response.

---

## Step 6: List Books

- Expand **GET /api/books**.
- Click **Try it out** and then **Execute**.
- Confirm your newly added books appear in the response.

---

## Step 7: User Management (Optional)

- Use the **Users** section to test endpoints like creating, modifying, or deleting users.
- Ensure you have the correct role (admin) authorized.
- Use **Try it out** and fill in required data for each endpoint.
- Execute and verify responses.

---

## Step 8: Test Utility Endpoints

- Test **GET /health** to check server health.
- Test **GET /** for welcome or root info.

---

## Tips for using Swagger UI

- Use the **Clear authorization** button to reset authentication tokens if needed.
- Always copy the freshest `access_token` after login for secure API access.
- Review the **Response body** and **Response code** after each request for confirmation.
- You can expand **Schemas** on the right side to understand expected input/output formats.

---

This guided approach ensures you comprehensively validate your APIs interactively using Swagger UI without manual curl commands.


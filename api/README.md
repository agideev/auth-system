<h1 align="center" style="font-weight: bold;">Auth System API</h1>

<p align="center">
  <a href="#technologies">Technologies</a> •
  <a href="#started">Getting Started</a> •
  <a href="#tests">Tests</a> •
  <a href="#routes">API Endpoints</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#contribute">Contribute</a>
</p>

<p align="center">
  <b>REST API for user authentication and account management, built with Python and Flask.</b>
</p>

---

<h2 id="technologies">💻 Technologies</h2>

* Python 3.10+
* Flask
* Flask Migrate
* MySQL
* SQLAlchemy
* PyMySQL
* Flask-JWT-Extended
* Pytest
* REST API

<h2 id="started">🚀 Getting Started</h2>

Follow the steps below to run the project locally.

<h3>Prerequisites</h3>

Before running the project, make sure you have installed:

* Python 3.10+
* MySQL 8+
* pip
* Git

<h3>Cloning</h3>

Clone the repository to your local machine:

```bash
# Clone the repository
git clone https://github.com/agideev/auth-system.git

# Navigate to the project directory
cd auth-system/api
```

<h3>Environment Variables</h3>

Create a <code>.env</code> file in the project root based on the <code>.env.example</code> file.

```env
JWT_SECRET_KEY=your_super_secret_jwt_key_here
DATABASE_URL=mysql+pymysql://username:password@localhost/database_name
```

Replace the example values with your actual environment configuration.

<h3>Virtual Environment</h3>

Create a Python virtual environment:

```bash
# Create the virtual environment
python3 -m venv .venv
```

Activate it:

```bash
# Linux / macOS
source .venv/bin/activate
```

For Windows:

```bash
# Windows
.venv\Scripts\activate
```

<h3>Installing Dependencies</h3>

Install the required Python packages:

```bash
pip install -r requirements.txt
```

<h3>Database & Migrations</h3>

The project uses **MySQL** as its database and **Flask-Migrate** to manage database schema changes.

Before running the migrations, make sure you have a MySQL database created for the project.

<h4>Creating the MySQL Database</h4>

Create a database in MySQL:

```sql
CREATE DATABASE auth_system;
```

Make sure the database name, username, password, and host match the <code>DATABASE_URL</code> configured in your <code>.env</code> file.

Example:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost/auth_system
```

<h4>Running Migrations</h4>

After configuring the database, apply the existing migrations:

```bash
flask db upgrade
```

This will create and update the required database tables according to the project's migration files.

<h4>Creating a New Migration</h4>

Whenever you make changes to the SQLAlchemy models, generate a new migration:

```bash
flask db migrate -m "describe your changes"
```

Then apply the migration:

```bash
flask db upgrade
```

<h4>Migration Workflow</h4>

The usual workflow when modifying the database models is:

```bash
# 1. Modify your SQLAlchemy models

# 2. Generate a migration
flask db migrate -m "describe your changes"

# 3. Apply the migration
flask db upgrade
```

> **Note:** The database itself must exist before running the migrations. The migration system creates and modifies the project's tables, but it does not create the MySQL database specified in <code>DATABASE_URL</code>.


<h3>Starting</h3>

Start the Flask API locally:

```bash
python run.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

---

<h2 id="tests">🧪 Tests</h2>

The project uses Pytest for automated testing.

Run all tests:

```bash
pytest
```

For detailed output:

```bash
pytest -v
```

---

<h2 id="routes">📍 API Endpoints</h2>

### Authentication

| Method | Endpoint    | Description                                    |
| ------ | ----------- | ---------------------------------------------- |
| `POST` | `/register` | Register a new user                            |
| `POST` | `/login`    | Authenticate a user and return an access token |

### User

| Method | Endpoint       | Description                              |
| ------ | -------------- | ---------------------------------------- |
| `GET`  | `/me`          | Get the authenticated user's profile     |
| `PUT`  | `/me`          | Update the authenticated user's profile  |
| `PUT`  | `/me/password` | Change the authenticated user's password |

### JWT Authentication

Protected endpoints require a valid JWT access token:

```http
Authorization: Bearer <access_token>
```

---

### `POST /register`

Registers a new user.

**Request:**

```json
{
  "username": "agi",
  "email": "agi@example.com",
  "password": "Example123"
}
```

**Response — `201 Created`:**

```json
{
  "success": true,
  "access_token": "token...",
  "message": "User registered successfully.",
  "user": {
    "id": 1,
    "username": "agi",
    "email": "agi@example.com"
  }
}
```

---

### `POST /login`

Authenticates a user and returns an access token.

**Request:**

```json
{
  "email": "agi@example.com",
  "password": "Example123"
}
```

**Response — `200 OK`:**

```json
{
  "success": true,
  "access_token": "token...",
  "message": "Login successful.",
  "user": {
    "id": 1,
    "username": "agi",
    "email": "agi@example.com"
  }
}
```

---

### `GET /me`

Returns the authenticated user's profile.

**Response — `200 OK`:**

```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "agi",
    "email": "agi@example.com",
    "is_active": true
  }
}
```

**Possible errors:**

* `401 Unauthorized` — JWT is missing or invalid.
* `404 Not Found` — User associated with the JWT does not exist.

---

### `PUT /me`

Updates the authenticated user's username and email.

**Request:**

```json
{
  "username": "new_username",
  "email": "new@example.com"
}
```

**Response — `200 OK`:**

```json
{
  "success": true,
  "message": "Profile updated successfully.",
  "user": {
    "id": 1,
    "username": "new_username",
    "email": "new@example.com",
    "is_active": true
  }
}
```

**Possible errors:**

* `400 Bad Request` — Invalid or already-used username/email.
* `401 Unauthorized` — JWT is missing or invalid.
* `404 Not Found` — User does not exist.

---

### `PUT /me/password`

Changes the authenticated user's password.

**Request:**

```json
{
  "current_password": "CurrentPassword123",
  "new_password": "NewPassword123"
}
```

**Response — `200 OK`:**

```json
{
  "success": true,
  "message": "Password updated successfully."
}
```

**Possible errors:**

* `400 Bad Request` — Current password is incorrect or the new password is invalid.
* `401 Unauthorized` — JWT is missing or invalid.
* `404 Not Found` — User does not exist.

---

<h2 id="project-structure">📁 Project Structure</h2>

The backend follows a modular Flask architecture:

```text
api/
│
├── app/
│   ├── models/
│   ├── routes/
│   └── ...
│
├── migrations/
│   └── versions/
│
├── tests/
│   └── test_auth.py
│
├── .env
├── .env.example
├── .gitignore
├── pyrightconfig.json
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

<h2 id="contribute">📫 Contribute</h2>

Contributions are welcome!

To contribute to the project:

1. Clone the repository.
2. Create a new branch:

```bash
git checkout -b feature/NAME
```

3. Make your changes and run the tests:

```bash
pytest -v
```

4. Commit your changes:

```bash
git add .
git commit -m "feat: describe your change"
```

5. Push your branch:

```bash
git push origin feature/NAME
```

6. Open a Pull Request describing the problem solved or feature implemented.

If your changes affect the API, update the relevant endpoint documentation.

---

<h3>📚 Documentation</h3>

* Flask Documentation
* Python Documentation
* Pytest Documentation
* Git Documentation

---

<h2 align="center">Auth System API</h2>

<p align="center">
  Built with Python, Flask, MySQL and JWT.
</p>

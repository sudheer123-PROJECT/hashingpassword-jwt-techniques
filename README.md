# FastAPI Secure Authentication System

A beginner-friendly full-stack authentication project built with **FastAPI, Python, SQLite, Argon2 password hashing, and JSON Web Tokens (JWT)**.

This project demonstrates how to securely register users, verify login credentials, issue JWT access tokens, and protect user-specific API endpoints.

## Features

- User registration with input validation
- Secure password hashing using Argon2
- Password verification during login
- JWT access token generation and validation
- Protected profile and dashboard endpoints
- Update profile username
- SQLite database integration using SQLAlchemy
- Frontend built with HTML, CSS, and JavaScript
- Token expiration and invalid-token handling
- API documentation through FastAPI Swagger UI

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| SQLAlchemy | Database ORM |
| SQLite | Data storage |
| Pydantic | Request validation |
| pwdlib + Argon2 | Password hashing |
| PyJWT | JWT authentication |
| HTML, CSS, JavaScript | Frontend development |

## Project Structure

```text
fastapi-secure-authentication/
├── frontend/
│   ├── register.html
│   ├── login.html
│   ├── profile.html
│   ├── style.css
│   └── script.js
├── main.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-secure-authentication.git
cd fastapi-secure-authentication
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the environment

Create a `.env` file in the project root.

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Add the generated value to `.env`:

```dotenv
SECRET_KEY=YOUR_GENERATED_SECRET_KEY
```

Never commit your actual `.env` file or secret key.

### 5. Start the backend

```bash
python -m uvicorn main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

### 6. Start the frontend

Open a second terminal from the project root:

```bash
python -m http.server 5500 --directory frontend
```

Open:

http://127.0.0.1:5500/register.html

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API health check |
| POST | `/register` | Register a new user |
| POST | `/login` | Authenticate user and issue JWT |
| GET | `/profile` | Retrieve authenticated user's profile |
| PUT | `/profile` | Update authenticated user's username |
| GET | `/dashboard` | Access protected dashboard endpoint |

Protected endpoints require a valid access token in the HTTP Authorization header:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Security Concepts Demonstrated

### Password Hashing

Passwords are hashed using Argon2 before being stored in the database. Login verifies the entered password against the stored hash instead of storing or comparing plaintext passwords.

### JWT Authentication

After successful login, the backend issues a signed JWT access token. Protected endpoints validate the token's signature and expiration before retrieving the associated user.

### Database Security

The application stores password hashes instead of original passwords and returns user profile data without exposing the password hash.

## Learning Outcomes

- Building REST APIs using FastAPI
- Connecting Python applications to SQLite
- Implementing password hashing and verification
- Creating and validating JWT access tokens
- Protecting API endpoints using authentication dependencies
- Connecting a JavaScript frontend to a Python backend
- Testing APIs with Swagger UI

## Future Improvements

- Password change and reset functionality
- Role-based authorization
- Refresh tokens and server-side token revocation
- Automated tests using pytest
- Deployment with HTTPS and production configuration
- Improved frontend session security

## Disclaimer

This project is intended for learning and portfolio demonstration. Before production use, implement appropriate HTTPS, secure session/token handling, rate limiting, secret management, and additional security testing.

## Author

**YOUR NAME**

GitHub: https://github.com/YOUR_USERNAME

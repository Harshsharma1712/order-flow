# Contributing Guide

Thank you for your interest in contributing to the **Order Flow**! 

Contributions of all kinds are welcome — whether it’s fixing bugs, improving documentation, optimizing code, or adding new features.

This guide will help you get started and ensure smooth collaboration.

---

## Code of Conduct

Please be respectful and professional in all interactions.

* Be constructive and kind
* Respect different viewpoints and experiences
* No harassment, hate speech, or personal attacks

By participating, you agree to follow these principles.

---

## How to Contribute

### 1. Fork the Repository

Click the **Fork** button on GitHub to create your own copy of the repository.

---

### 2. Clone Your Fork

```bash
git clone https://github.com/Harshsharma1712/order-flow
cd order-flow
```

---

### 3. Create a New Branch

Always create a new branch for your changes:

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:

* `feature/` → New features
* `fix/` → Bug fixes
* `docs/` → Documentation changes
* `refactor/` → Code refactoring

---

### 4. Set Up the Development Environment

#### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Environment Variables

Create a `.env` file:

```env
DATABASE_URL= postgresql+asyncpg
SECRET_KEY= your_secret_key
ALGORITHM= HS256
ACCESS_TOKEN_EXPIRE_MINUTES= 
RESEND_API_KEY=
```

---

### 5. Run Database Migrations

```bash
alembic upgrade head
```

---

### 6. Start the Development Server

```bash
uvicorn app.main:app --reload
```

Server will be available at:

```
http://127.0.0.1:8000
```

---

## Coding Standards

Please follow these conventions:

### Python & FastAPI

* Follow **PEP 8** style guidelines
* Use **type hints** wherever possible
* Keep endpoints thin; move business logic to services
* Use dependency injection properly

### Database

* Use SQLAlchemy ORM patterns
* Avoid raw SQL unless absolutely necessary
* All schema changes must go through **Alembic migrations**

### API Design

* Use RESTful naming conventions
* Return proper HTTP status codes
* Validate all inputs using **Pydantic schemas**

---

## Commit Message Guidelines

Write clear and meaningful commit messages:

```
feat: add order cancellation endpoint
fix: resolve email notification bug
refactor: optimize order status update logic
docs: update README setup instructions
```

---

## Submitting a Pull Request

Before opening a PR, ensure:

* Code is well-formatted and linted
* No sensitive data is committed (`.env`, secrets)
* All existing functionality works as expected

### Pull Request Steps

1. Push your branch to your fork
2. Open a Pull Request against the `main` branch
3. Clearly describe:

   * What you changed
   * Why the change is needed
   * Any breaking changes

---

## Security Issues

If you discover a security vulnerability:

* **Do not** open a public issue
* Please report it privately to the repository maintainer

---

## Thank You

Your contributions help make this project better for everyone.

If you’re new to open source, don’t hesitate to ask questions or open a draft PR — we’re happy to help!

Happy coding

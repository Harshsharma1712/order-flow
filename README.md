# Order Flow

A **role-based order management backend** built with **FastAPI** that allows local shops to manage orders efficiently and customers to avoid physical queues. The system supports **shop owners** creating shops and items, and **normal users** placing orders and receiving **email notifications** when items are ready or picked up.

This project is currently **backend-only** and designed to be easily extended with a frontend in the future.

---

## Problem Statement

Local shops often struggle with long queues and inefficient order handling. Customers waste time waiting, and shop owners find it hard to manage order status updates.

This backend system solves that by:

* Allowing customers to **order remotely**
* Enabling shop owners to **manage orders digitally**
* Sending **email notifications** when an order status changes

---

## Features

### Authentication & Roles

* JWT-based authentication
* Two user roles:

  * **Normal User** – can browse shops and place orders
  * **Shop Owner** – can create shops, add items, and manage orders

### Shop Management (Shop Owner)

* Create and manage a shop
* Add, update, and list items
* View orders placed for their shop
* Update order status (e.g., *Ready*, *Picked Up*)

### Ordering System (Normal User)

* Browse shops and items
* Place orders for items
* Track order status

### Email Notifications

* Automated email notifications using **Resend**
* Emails sent to users when:

  * Order is marked as **Ready**
  * Order is **Picked Up**

### Database & Migrations

* PostgreSQL as the primary database
* SQLAlchemy ORM for database interactions
* Alembic for schema migrations

---

## Tech Stack

* **Backend Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Authentication:** JWT (JSON Web Tokens)
* **Email Service:** Resend
* **Data Validation:** Pydantic

---


## Setup & Installation

### Clone the Repository

```bash
git clone https://github.com/Harshsharma1712/order-flow
cd order-flow
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file and configure the following:

```env
DATABASE_URL= postgresql+asyncpg
SECRET_KEY= your_secret_key
ALGORITHM= HS256
ACCESS_TOKEN_EXPIRE_MINUTES= 
RESEND_API_KEY= 
```

### Run Database Migrations

```bash
alembic upgrade head
```

### Start the Server

```bash
uvicorn app.main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

Swagger Docs:

```
http://127.0.0.1:8000/docs
```

---

## Authentication Flow

1. User registers as **Normal User** or **Shop Owner**
2. User logs in and receives a **JWT access token**
3. Token is required for all protected endpoints
4. Role-based access control ensures proper authorization

---

## API Documentation

* Interactive API docs available via **Swagger UI**
* Includes request/response schemas and authentication support

---

## Use Case

This system is ideal for:

* Small local shops
* Cafes and takeaway stores
* Any business where customers usually wait in queues

---

## Contributing

For complete guide reffer contributing guide

Contributions are welcome!

* Fork the repository
* Create a feature branch
* Commit changes
* Open a Pull Request

---

## License

This project is licensed under the **MIT License**.

---

## Acknowledgements

* FastAPI Documentation
* SQLAlchemy
* Resend Email API

---

If you find this project useful, feel free to Star the repository!

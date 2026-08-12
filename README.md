# Customer Support & Ticket Management System

A backend REST API built with FastAPI for managing customer support tickets with authentication, role-based access control, MongoDB, validation, logging, and automated testing.

## Features

- User registration and login
- JWT-based authentication
- Role-based access control (RBAC)
- Create support tickets
- View all tickets
- View individual tickets
- Update tickets
- Delete tickets
- Search tickets
- Filter tickets by priority and status
- Pagination
- Request validation
- Custom exception handling
- Application logging
- MongoDB database
- Automated API tests with Pytest

## Tech Stack

- Python
- FastAPI
- MongoDB
- PyMongo
- JWT Authentication
- Pydantic
- Pytest
- Uvicorn

## Project Structure

```text
customer-support-system/
│
├── app/
│   ├── api/
│   ├── auth/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── tests/
│   ├── test_api.py
│   ├── test_auth.py
│   └── test_tickets.py
│
├── .gitignore
├── requirements.txt
└── README.md

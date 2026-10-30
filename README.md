# Personal Expense Tracker API

A RESTful backend API built using **Python, Flask, PostgreSQL, SQLAlchemy, and Pydantic** to manage daily expenses.

The project follows a layered architecture with separate routes, services, repositories, models, and schemas to improve maintainability, testability, and code organization.

## Features

- Create, retrieve, update, and delete expenses
- Validate request data using Pydantic
- Filter expenses by category and date range
- Paginate expense records
- Generate monthly expense summaries grouped by category
- Handle API and database errors through centralized exception handling
- Manage PostgreSQL schema changes using Flask-Migrate and Alembic
- Test API functionality using pytest

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Programming language |
| Flask | REST API framework |
| PostgreSQL | Relational database |
| Flask-SQLAlchemy | ORM and database integration |
| Pydantic v2 | Request validation and data schemas |
| Flask-Migrate / Alembic | Database migrations |
| psycopg | PostgreSQL driver |
| pytest | Automated testing |
| Postman | Manual API testing |

## Project Architecture

```text
personal-expense-tracker-api/
├── app/
│   ├── exceptions/
│   │   ├── api_exceptions.py
│   │   └── handlers.py
│   ├── models/
│   │   └── expense.py
│   ├── repositories/
│   │   └── expense_repository.py
│   ├── routes/
│   │   └── expense_routes.py
│   ├── schemas/
│   │   ├── expense_schema.py
│   │   └── response_schema.py
│   ├── services/
│   │   └── expense_service.py
│   ├── utils/
│   │   ├── request_parser.py
│   │   ├── response_builder.py
│   │   ├── serializers.py
│   │   └── validators.py
│   ├── config.py
│   ├── extensions.py
│   └── __init__.py
├── migrations/
├── postman/
├── tests/
│   ├── conftest.py
│   └── test_expenses.py
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

### Request Flow

```text
Client / Postman
       |
       v
Flask Routes
       |
       v
Pydantic Validation
       |
       v
Service Layer
       |
       v
Repository Layer
       |
       v
SQLAlchemy Models
       |
       v
PostgreSQL
```

**Routes:** Handle incoming HTTP requests and return API responses.

**Schemas:** Validate request parameters and expense data.

**Services:** Implement business logic and coordinate database operations.

**Repositories:** Encapsulate database queries.

**Models:** Define database tables and constraints.

**Exception handlers:** Provide centralized error handling.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/Shah-Vansh/personal-expense-tracker-api.git
cd personal-expense-tracker-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows CMD:

```cmd
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL role with an appropriate password and a database named `expense_tracker_db`.

Ensure the application role has permission to create and modify tables in the application's schema.

### 5. Configure environment variables

Copy `.env.example` to `.env`:

```cmd
copy .env.example .env
```

Configure the database URLs:

```dotenv
DATABASE_URL=postgresql+psycopg://expense_app:YOUR_PASSWORD@localhost:5432/expense_tracker_db
TEST_DATABASE_URL=postgresql+psycopg://expense_app:YOUR_PASSWORD@localhost:5432/expense_tracker_test
```

Replace `YOUR_PASSWORD` with the URL-encoded PostgreSQL password for `expense_app`.

Never commit `.env` or real database credentials.

### 6. Apply database migrations

For a new, empty application database:

```bash
python -m flask --app run:app db upgrade
```

The initial migration revision is:

```text
5b764e4ef81f
```

Do not stamp an existing database without first verifying that its schema matches the migration baseline.

### 7. Start the application

```bash
python run.py
```

The development API runs at:

```text
http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/expenses` | Retrieve expenses |
| POST | `/expenses` | Create an expense |
| GET | `/expenses/{id}` | Retrieve an expense by ID |
| PUT | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |
| GET | `/expenses/summary/monthly` | Generate monthly expense summary |

### Create Expense

**POST** `/expenses`

Example request:

```json
{
  "amount": "250.00",
  "category": "Food",
  "date": "2026-10-24",
  "description": "Lunch"
}
```

### Filter Expenses

**GET** `/expenses?category=Food`

Filter by date range:

```text
GET /expenses?start_date=2026-10-01&end_date=2026-10-31
```

### Pagination

**GET** `/expenses?page=1&limit=10`

Supported pagination parameters:

- `page`: Positive integer, default `1`
- `limit`: Integer from `1` to `100`, default `10`

Paginated responses include record counts, page information, and expense data.

### Monthly Summary

**GET** `/expenses/summary/monthly?year=2026&month=10`

Example response:

```json
{
  "success": true,
  "message": "Monthly expense summary retrieved successfully",
  "data": {
    "year": 2026,
    "month": 10,
    "total": "600.50",
    "transaction_count": 2,
    "categories": [
      {
        "category": "Food",
        "count": 1,
        "total": "250.00"
      },
      {
        "category": "Travel",
        "count": 1,
        "total": "350.50"
      }
    ]
  },
  "error": null
}
```

## Automated Testing

The project uses pytest with a separate PostgreSQL test database.

Create an empty database named `expense_tracker_test`, owned by the application database role, before running the tests.

**Warning:** Automated tests create and drop tables in the test database. Never configure the tests to use the development or production database.

Run the full test suite:

```bash
python -m pytest tests/ -v
```

Current verified result:

```text
26 passed
```

The tests cover CRUD operations, request validation, missing records, filtering, pagination, monthly summaries, and edge cases.

## Database Migrations

Generate a migration after modifying database models:

```bash
python -m flask --app run:app db migrate -m "describe schema change"
```

Review the generated migration before applying it.

Apply migrations:

```bash
python -m flask --app run:app db upgrade
```

Check migration status:

```bash
python -m flask --app run:app db current
```

## API Testing with Postman

Postman can be used to test all API endpoints.

The `postman/` directory is intended to contain the project's API collection and local environment configuration. Export these files without real credentials before sharing the repository.

## Security and Development Notes

- Keep database credentials in `.env`.
- Do not commit database backups or virtual environments.
- Use parameterized ORM queries.
- Validate request data before processing it.
- Use a dedicated database for automated tests.
- Review migrations before applying them to databases containing data.

## Project Status

The core Expense Tracker API functionality is implemented, with 26 automated tests passing.

The project is under continued development and code review.
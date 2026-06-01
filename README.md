# FastAPI CRUD API

A simple FastAPI CRUD application with:

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Swagger/OpenAPI Documentation

---

## Project Structure

```text
fastapi-app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── routes/
│       ├── __init__.py
│       └── items.py
│
├── tests/
│   ├── __init__.py
│   └── test_items.py
│
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Features

- Create Item
- Get All Items
- Get Single Item
- Update Item
- Delete Item
- Automatic Swagger Documentation
- Unit Tests with Pytest

---

## API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "status": "ok"
}
```

---

### Create Item

```http
POST /items/
```

Request:

```json
{
  "name": "Laptop",
  "description": "MacBook Pro"
}
```

Response:

```json
{
  "id": 1,
  "name": "Laptop",
  "description": "MacBook Pro"
}
```

---

### Get All Items

```http
GET /items/
```

Response:

```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "MacBook Pro"
  }
]
```

---

### Get Item By ID

```http
GET /items/{id}
```

Response:

```json
{
  "id": 1,
  "name": "Laptop",
  "description": "MacBook Pro"
}
```

---

### Update Item

```http
PUT /items/{id}
```

Request:

```json
{
  "name": "Updated Laptop",
  "description": "Updated Description"
}
```

Response:

```json
{
  "id": 1,
  "name": "Updated Laptop",
  "description": "Updated Description"
}
```

---

### Delete Item

```http
DELETE /items/{id}
```

Response:

```json
{
  "message": "Deleted successfully"
}
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/fastapi-app.git

cd fastapi-app
```

### Create Virtual Environment

Windows:

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux/Mac:

```bash
python -m venv .venv

source .venv/bin/activate
```

### Install Dependencies

Using pip:

```bash
pip install -r requirements.txt
```

Using uv:

```bash
uv pip install -r requirements.txt
```

---

## Running the Application

```bash
uvicorn app.main:app --reload
```

Application URL:

```text
http://localhost:8000
```

---

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Verbose output:

```bash
pytest -v
```

Coverage:

```bash
pytest --cov=app
```

---

## Example cURL Commands

### Create Item

```bash
curl -X POST "http://localhost:8000/items/" \
-H "Content-Type: application/json" \
-d '{
  "name":"Laptop",
  "description":"MacBook Pro"
}'
```

### Get Items

```bash
curl http://localhost:8000/items/
```

### Update Item

```bash
curl -X PUT "http://localhost:8000/items/1" \
-H "Content-Type: application/json" \
-d '{
  "name":"Updated Laptop",
  "description":"Updated"
}'
```

### Delete Item

```bash
curl -X DELETE "http://localhost:8000/items/1"
```

---

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest
- Uvicorn

---

## Development

Format code:

```bash
black .
```

Lint code:

```bash
ruff check .
```

Run tests:

```bash
pytest
```

---

## License

MIT License

---

## Author

Your Name

GitHub: https://github.com/yourusername

For production projects, I'd also recommend adding:

├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── alembic/
├── app/
│ ├── core/
│ ├── api/
│ ├── services/
│ ├── repositories/
│ ├── schemas/
│ ├── models/
│ └── tests/

This structure scales much better for SaaS and enterprise FastAPI applications.

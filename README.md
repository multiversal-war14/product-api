# Product API

A Django REST Framework backend for managing products.

## Features

* Product CRUD operations
* Search products by partial name
* Filter products by minimum and maximum price
* Pagination with configurable page size
* Product purchase endpoint
* Stock validation
* Error handling
* Automated tests

## Technologies

* Python
* Django
* Django REST Framework
* SQLite

## Setup

### 1. Create and activate the virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install django djangorestframework
```

### 3. Run migrations

```powershell
python manage.py migrate
```

### 4. Start the server

```powershell
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/`

## API Endpoints

| Method | Endpoint                       | Description              |
| ------ | ------------------------------ | ------------------------ |
| GET    | `/api/products/`               | List products            |
| POST   | `/api/products/`               | Create product           |
| GET    | `/api/products/<id>/`          | Get a product            |
| PUT    | `/api/products/<id>/`          | Update product           |
| PATCH  | `/api/products/<id>/`          | Partially update product |
| DELETE | `/api/products/<id>/`          | Delete product           |
| POST   | `/api/products/<id>/purchase/` | Purchase product         |

## Search

Search products by name:

`GET /api/products/?search=mouse`

The search is case-insensitive and supports partial matches.

## Price Filtering

Minimum price:

`GET /api/products/?min_price=700`

Maximum price:

`GET /api/products/?max_price=1000`

Both filters:

`GET /api/products/?min_price=700&max_price=1000`

## Pagination

Pagination supports a configurable page size:

`GET /api/products/?page=1&page_size=1`

The maximum page size is 10.

## Purchase

To purchase a product, send a POST request:

`POST /api/products/1/purchase/`

with:

```json
{
    "quantity": 3
}
```

The requested quantity is deducted from the product stock.

The API returns an error if the requested quantity is greater than the available stock.

## Error Handling

The API returns appropriate HTTP status codes for invalid requests, including:

* `400 Bad Request` for invalid purchase quantities or insufficient stock
* `404 Not Found` when a requested product does not exist

## Testing

Run the automated tests with:

```powershell
python manage.py test products
```

The project includes tests for:

* Product listing
* Product search
* Stock reduction after purchase
* Insufficient stock handling

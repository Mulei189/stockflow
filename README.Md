# StockFlow API

StockFlow is an inventory and sales management backend built with
Python, FastAPI and PostgreSQL.

## Features

- Authentication
- Product management
- Category management
- Supplier management
- Customer management
- Purchase management
- Sales management
- Automatic stock updates
- Stock movement tracking
- Inventory monitoring
- Low-stock detection
- Out-of-stock detection
- Sales analytics
- Product analytics
- Customer analytics
- Purchase analytics
- Management dashboard analytics

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT Authentication
- Neon PostgreSQL

## Architecture

The application follows a modular architecture where each
business domain owns its models, schemas, services and routes.

## API Documentation

Once running:

- `/docs`
- `/redoc`

## Running Locally

```bash
git clone <repository-url>

cd inventory-and-sales_API

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

python -m uvicorn main:app --reload
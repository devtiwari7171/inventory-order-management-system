# Inventory & Order Management System

A full-stack web application for managing products, customers, orders, and inventory. Built as part of a technical assessment to demonstrate end-to-end full-stack skills with Python, React, PostgreSQL, and Docker.

**Live demo:**
- Frontend: https://inventory-frontend-one-drab.vercel.app
- Backend API: https://inventory-order-management-system-hnpm.onrender.com
- API docs (Swagger): https://inventory-order-management-system-hnpm.onrender.com/docs

---

## What this app does

It's a back-office tool for a small business that sells physical products. Three main entities:

- **Products** — what you sell (name, SKU, price, stock level)
- **Customers** — who buys from you (name, email, phone)
- **Orders** — what they bought and when

The interesting part is the **inventory tracking**: when you create an order, the stock count for each product is automatically reduced. If you try to order more than what's in stock, the API returns a 400 error and nothing changes. If you cancel an order, the stock is restored.

The dashboard at the top of the page shows totals and a list of low-stock items so you know what to reorder.

---

## Tech stack

Backend:
- Python 3.11
- FastAPI
- SQLAlchemy 2.0 (ORM)
- Alembic (migrations)
- Pydantic (validation)
- PostgreSQL 16

Frontend:
- React 18 (JavaScript)
- Vite 5
- React Router 6
- Axios
- Tailwind CSS

Infrastructure:
- Docker + Docker Compose
- pytest (backend tests)

Deployment (all free tiers):
- Database → Neon
- Backend → Render
- Frontend → Vercel
- Backend image → Docker Hub

---

## Project structure

```
inventory-order-management-system/
├── backend/
│   ├── app/
│   │   ├── core/           # config + database engine
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic request/response models
│   │   ├── repositories/   # data access layer
│   │   ├── services/       # business logic
│   │   ├── api/            # FastAPI routers
│   │   ├── exceptions.py
│   │   └── main.py
│   ├── alembic/            # DB migrations
│   ├── tests/              # pytest suite
│   ├── Dockerfile
│   ├── entrypoint.sh       # waits for DB → migrates → starts server
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/            # axios instance
│   │   ├── services/       # API service layer
│   │   ├── hooks/          # custom React hooks
│   │   ├── components/     # reusable UI
│   │   ├── pages/          # Dashboard, Products, Customers, Orders
│   │   └── utils/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── .env.example
├── docker-compose.yml
└── DEPLOYMENT.md           # step-by-step deployment guide
```

The backend is organized as a 4-layer architecture: routes → services → repositories → models. Each layer has one job, and FastAPI's `Depends()` wires them together. This makes it easy to unit-test the business logic without touching HTTP or the database.

The frontend uses a similar separation: services (axios calls) → hooks (state + loading/error) → components → pages.

---

## API endpoints

Base URL: `/api/v1`

Products
- `POST /products` — create
- `GET /products` — list (with optional `?q=` for search)
- `GET /products/{id}` — get one
- `PUT /products/{id}` — update
- `DELETE /products/{id}` — delete

Customers
- `POST /customers` — create
- `GET /customers` — list
- `GET /customers/{id}` — get one
- `DELETE /customers/{id}` — delete (blocked if customer has orders)

Orders
- `POST /orders` — create (validates stock, decrements inventory, atomic transaction)
- `GET /orders` — list
- `GET /orders/{id}` — get one with line items
- `DELETE /orders/{id}` — cancel (restores stock)

Dashboard
- `GET /dashboard` — totals + low-stock list

Status codes used:
- 200 / 201 / 204 for success
- 400 for business rule violations (e.g. insufficient stock)
- 404 for missing resources
- 409 for duplicates (SKU, email)
- 422 for validation errors

---

## Database schema

Four tables with proper foreign keys and CHECK constraints:

```
customers (id, name, email UNIQUE, phone, created_at, updated_at)
   ↓ 1:N
orders (id, customer_id FK, total_amount, created_at, updated_at)
   ↓ 1:N
order_items (id, order_id FK CASCADE, product_id FK, quantity > 0,
             unit_price >= 0, subtotal >= 0)
   ↑ N:1
products (id, name, sku UNIQUE, price >= 0, stock_quantity >= 0,
          created_at, updated_at)
```

The schema is defined in `backend/alembic/versions/0001_initial.py` and gets created on deploy via `alembic upgrade head` in the entrypoint script.

---

## Running it locally

You need Docker (or Docker Desktop on Windows/Mac) installed. PostgreSQL and Node are not required since the compose file brings them up.

```bash
git clone https://github.com/<your-username>/inventory-order-management-system.git
cd inventory-order-management-system
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
docker compose up --build
```

Then open http://localhost:3000

If you'd rather run things manually without Docker (useful when hacking on the code):

```bash
# Terminal 1 — Postgres only
docker run -d --name inv-pg \
  -e POSTGRES_USER=inventory_user \
  -e POSTGRES_PASSWORD=inventory_password \
  -e POSTGRES_DB=inventory_db \
  -p 5432:5432 postgres:16-alpine

# Terminal 2 — Backend
cd backend
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Terminal 3 — Frontend
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## Running tests

```bash
cd backend
pytest -v
```

29 tests covering product CRUD, customer CRUD, order creation with stock validation, order cancellation with stock restoration, dashboard aggregation, and the usual edge cases (duplicate SKU, invalid email, insufficient stock, unknown IDs, zero quantity).

---

## Business rules implemented

- Product SKU must be unique — enforced at DB level (`UNIQUE` constraint) and in the service layer
- Customer email must be unique and valid — enforced by Pydantic `EmailStr` plus a unique index
- Price and stock cannot be negative — enforced by CHECK constraints in PostgreSQL and field validators in Pydantic
- Orders can't be created if stock is insufficient — checked before any writes, returns 400 with a clear message
- Stock is automatically decremented on order creation — happens in the same transaction as the order insert
- Total amount is computed by the backend (sum of quantity × unit_price for each line)
- Order cancellation restores stock — same atomic-transaction pattern as creation

All multi-step database operations (order create, order cancel) are wrapped in try/except with explicit rollback on failure, so a failure halfway through leaves the database untouched.

---

## Deployment

See `DEPLOYMENT.md` for the full step-by-step guide. Quick summary:

1. **Database** — Created a free Neon project at neon.tech and ran `alembic upgrade head` against it to create the tables.
2. **Backend** — Connected the GitHub repo to Render as a Docker web service. Set the `DATABASE_URL` env var to the Neon connection string. The `entrypoint.sh` waits for the DB, runs migrations, then starts uvicorn.
3. **Frontend** — Connected the GitHub repo to Vercel, set `VITE_API_URL` to the Render backend URL, and deployed.
4. **Docker Hub** — Built the backend image locally with `docker build -t <user>/inventory-backend:latest .` and pushed with `docker push`.
5. **CORS** — Set `ALLOWED_ORIGINS` on Render to the Vercel URL so the frontend can call the backend.

Free-tier caveat: Render puts the service to sleep after 15 minutes of inactivity, so the first request after a break takes ~30 seconds to wake up. This is expected behavior.

---

## Things I would do differently / future improvements

- Add JWT auth + role-based access (admin vs staff). Right now anyone with the URL can hit the API.
- Add sales analytics charts on the dashboard (revenue over time, top-selling products).
- CSV export for products and orders.
- Bulk product import from CSV.
- Email notifications when stock drops below a threshold.
- Pagination on the list endpoints — right now everything is returned in one page up to 200 items.
- The frontend shows customer ID instead of customer name in the order list because I didn't add a `/customers/{id}` lookup on the orders page. Would need a small refactor.

---

## Environment variables

**Backend** (`.env` in `backend/`):
```
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=any-random-string
ALLOWED_ORIGINS=https://your-frontend.vercel.app
POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT
DEBUG=False
```

**Frontend** (`.env` in `frontend/`):
```
VITE_API_URL=https://your-backend.onrender.com/api/v1
```

`.env.example` files are committed with placeholder values. Real `.env` files are in `.gitignore` and never committed.

---

## License

MIT

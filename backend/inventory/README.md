# Inventory Service (Rust)

A microservice for inventory management built with Rust and Actix-web.

## Features

- Track product stock levels
- Increase/decrease stock with audit trail
- Set absolute stock quantities
- Low stock alerts
- Movement history tracking

## Tech Stack

- **Language**: Rust
- **Framework**: Actix-web 4
- **Database**: PostgreSQL with SQLx
- **Async Runtime**: Tokio

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/inventory` | List all inventory items |
| GET | `/inventory/{product_id}` | Get inventory for a product |
| POST | `/inventory/{product_id}/increase` | Increase stock |
| POST | `/inventory/{product_id}/decrease` | Decrease stock |
| PUT | `/inventory/{product_id}` | Set absolute stock |
| GET | `/health` | Health check |

## Request/Response Examples

### Increase Stock
```bash
POST /inventory/1/increase
Content-Type: application/json

{
  "quantity": 10
}
```

### Decrease Stock
```bash
POST /inventory/1/decrease
Content-Type: application/json

{
  "quantity": 5
}
```

### Set Stock
```bash
PUT /inventory/1
Content-Type: application/json

{
  "quantity": 100,
  "reason": "Inventory count adjustment"
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8003` |
| `RUST_LOG` | Log level | `info` |

## Development

```bash
# Run locally
cargo run

# Build release
cargo build --release
```

## Docker

The service is containerized and runs as part of the multi-service Docker Compose setup.

```bash
# From project root
docker-compose up inventory
```


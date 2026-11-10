# ShopEase User Management Microservice

An independent FastAPI microservice responsible for managing customer profiles, contact numbers, and delivery addresses within the ShopEase e-commerce platform.

## Architecture & Tech Stack
- **Framework:** FastAPI (Python 3.11)
- **Database:** MySQL 8.0 (\shopease_user_db\)
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **Authentication:** JWT (Stateless Bearer Token validation sharing SECRET_KEY and ALGORITHM with Authentication Service)
- **Containerization:** Docker & Docker Compose

## Port Mappings
- **User Service:** \http://localhost:8002\ (Interactive Docs: \/docs\)
- **User MySQL DB:** \localhost:3310\ (mapped from internal port 3306)

## API Endpoints Matrix

### User Profile APIs
| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| **POST** | \/api/users/profile\ | Create user profile (auto-bound to JWT \uth_user_id\) | \201\, \400\, \401\ |
| **GET** | \/api/users/profile\ | Retrieve current authenticated user profile | \200\, \401\, \404\ |
| **PUT** | \/api/users/profile\ | Fully update profile information | \200\, \401\, \404\ |
| **PATCH** | \/api/users/profile\ | Partially update profile / contact details | \200\, \401\, \404\ |
| **DELETE** | \/api/users/profile\ | Delete user profile and cascade addresses | \200\, \401\, \404\ |

### User Address Management APIs
| Method | Endpoint | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| **POST** | \/api/users/addresses\ | Add new delivery address (auto-sets first address as default) | \201\, \401\, \404\ |
| **GET** | \/api/users/addresses\ | List all delivery addresses of authenticated user | \200\, \401\, \404\ |
| **GET** | \/api/users/addresses/{id}\ | Retrieve a specific address (enforces ownership) | \200\, \401\, \404\ |
| **PUT** | \/api/users/addresses/{id}\ | Update an existing address | \200\, \401\, \404\ |
| **PATCH** | \/api/users/addresses/{id}/default\ | Promote address to default (clears other defaults) | \200\, \401\, \404\ |
| **DELETE** | \/api/users/addresses/{id}\ | Delete address (promotes next address if default was removed) | \200\, \401\, \404\ |

## Docker Setup & Execution
\\\ash
# Build and run containers
docker compose up -d --build

# Inspect container status
docker compose ps
\\\

## Alembic Migrations
\\\ash
# Generate migration
docker compose exec user_service alembic revision --autogenerate -m "create user profiles and addresses tables"

# Apply migration
docker compose exec user_service alembic upgrade head
\\\

## Automated Test Results (16/16 Passed)
- Scenarios 1 & 2: Missing and invalid JWT tokens rejected with \401 Unauthorized\.
- Scenario 3: Profile created successfully with \201 Created\ and linked to \uth_user_id\.
- Scenario 4: Duplicate profile creation blocked with \400 Bad Request\.
- Scenarios 5, 6, 7: Profile retrieval, full update, and partial PATCH validated with \200 OK\.
- Scenarios 8, 9, 10: Multi-address addition and listing verified with automatic default assignment.
- Scenarios 11, 12, 13: Address update and default toggling validated with strict single-default rule enforcement.
- Scenarios 14 & 15: Cross-user profile and address isolation verified (access denied to unauthorized user IDs).
- Scenario 16: Address deletion verified.

## Account Deactivation & Cross-Service Consistency
- **User Service Role:** When a user's profile is deactivated (\is_active = False\) via \PATCH /api/users/profile\, the record and historical address relations remain intact for compliance, auditing, and pending order fulfillment.
- **Authentication Service Separation:** Deactivating the profile does not silently drop or corrupt the user credentials record in the Authentication Service (\shopease_auth_db\).
- **Distributed Status Handling:** 
  1. The User Service marks \UserProfile.is_active = False\ locally.
  2. In production with an API Gateway or event bus (e.g., Kafka/RabbitMQ), a \user.deactivated\ event is dispatched to trigger the Auth Service to revoke active refresh tokens and set \User.is_active = False\ in the auth database, preventing future login sessions while preserving data integrity across boundaries.

## Account Deactivation & Cross-Service Consistency
- **User Service Role:** When a user's profile is deactivated (\is_active = False\) via \PATCH /api/users/profile\, the record and historical address relations remain intact for compliance, auditing, and pending order fulfillment.
- **Authentication Service Separation:** Deactivating the profile does not silently drop or corrupt the user credentials record in the Authentication Service (\shopease_auth_db\).
- **Distributed Status Handling:** 
  1. The User Service marks \UserProfile.is_active = False\ locally.
  2. In production with an API Gateway or event bus (e.g., Kafka/RabbitMQ), a \user.deactivated\ event is dispatched to trigger the Auth Service to revoke active refresh tokens and set \User.is_active = False\ in the auth database, preventing future login sessions while preserving data integrity across boundaries.

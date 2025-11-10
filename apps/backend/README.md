# Backend Service

This document provides instructions on how to set up and run the backend service.

## Installation

1.  **Navigate to the backend directory:**
    ```bash
    cd apps/backend
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        source .venv/Scripts/activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You might need to create a `requirements.txt` file if it doesn't exist, by running `pip freeze > requirements.txt` after installing necessary packages.)*

## Database Setup with Docker

Before running the application, you need to set up the PostgreSQL database in a Docker container.

### Prerequisites

- Docker and Docker Compose installed on your machine
- Navigate to the `database` directory from the project root

### Steps to Start the Database

1.  **From the project root, navigate to the database directory:**
    ```bash
    cd database
    ```

2.  **Start the PostgreSQL container:**
    ```bash
    docker-compose up -d
    ```
    This will start a PostgreSQL container with:
    - Username: `capoo_user`
    - Password: `capoo_password`
    - Database: `capoo_db`
    - Port: `5432`

3.  **Verify the container is running:**
    ```bash
    docker-compose ps
    ```

### Database Connection Details

The database is automatically configured with your backend through the `.env` file. The connection string is:
```
DATABASE_URL=postgresql+psycopg2://capoo_user:capoo_password@localhost:5432/capoo_db
```

All SQL schemas from the database directory will be automatically initialized when the container starts.

### Stopping the Database

To stop the PostgreSQL container:
```bash
docker-compose down
```

To stop and remove all data:
```bash
docker-compose down -v
```

## Running the Application

1.  **Ensure your virtual environment is activated.**

2.  **Ensure the PostgreSQL database is running** (see "Database Setup with Docker" section above).

3.  **Run the FastAPI application using Uvicorn:**
    ```bash
    uvicorn app.main:app --reload
    ```
    This will start the server, typically accessible at `http://127.0.0.1:8000`. The `--reload` flag enables auto-reloading on code changes.

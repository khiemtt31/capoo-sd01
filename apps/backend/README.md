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

## Running the Application

1.  **Ensure your virtual environment is activated.**

2.  **Run the FastAPI application using Uvicorn:**
    ```bash
    uvicorn app.main:app --reload
    ```
    This will start the server, typically accessible at `http://127.0.0.1:8000`. The `--reload` flag enables auto-reloading on code changes.

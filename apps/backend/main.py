import uvicorn
from app.main import app

if __name__ == "__main__":
    # Run the application using Uvicorn
    # We use the app object defined in apps/backend/app/main.py
    uvicorn.run(app, host="0.0.0.0", port=8000)
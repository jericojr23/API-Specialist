# main.py
from fastapi import FastAPI
from routes.user_routes import router  # Import router as it is defined
from routes.task_routes import router

app = FastAPI()

# Include the router
app.include_router(router)

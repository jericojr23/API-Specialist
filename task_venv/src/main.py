from fastapi import FastAPI, HTTPException, status
from routes.user import user_router  # Import router as it is defined
from routes.task import task_router

app = FastAPI()

# Include the router
app.include_router(user_router)
app.include_router(task_router)

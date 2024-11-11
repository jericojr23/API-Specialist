from fastapi import FastAPI
from controllers.user_controller import router as user_router

app = FastAPI()

# Include the user router
app.include_router(user_router)

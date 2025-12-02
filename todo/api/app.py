from fastapi import FastAPI
from .routers import router as api_router

app = FastAPI(
    title="Todo List API",
    version="1.0.0"
)

# main router
app.include_router(api_router)

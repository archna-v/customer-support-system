from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.ticket_routes import router as ticket_router
from app.auth.auth_routes import router as auth_router
from app.core.logger import logger

from app.core.exception_handlers import (
    validation_exception_handler,
    general_exception_handler
)


app = FastAPI(
    title="Customer Support & Ticket Management System",
    description="Backend API for managing customer support tickets",
    version="1.0.0"
)


app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)


@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {
        "message": "Customer Support System API is running"
    }


app.include_router(ticket_router)
app.include_router(auth_router)
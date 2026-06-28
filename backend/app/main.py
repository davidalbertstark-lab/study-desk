# Standard/FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Core
from app.core.responses import success_response
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)

# Database
from app.db.init_db import init_db

# Routers
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as user_router
from app.modules.departments.router import router as dept_router
from app.modules.waitlist.router import router as waitlist_router

app = FastAPI(title="Study Desk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5175",
        "http://127.0.0.1:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# STARTUP EVENT (DB INIT)
# =========================
@app.on_event("startup")
def startup():
    init_db()


# =========================
# GLOBAL EXCEPTION HANDLERS
# =========================
app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    general_exception_handler
)


# =========================
# ROUTERS
# =========================

# Users (admin/general)
app.include_router(user_router)

# Authentication
app.include_router(auth_router)

app.include_router(dept_router)

app.include_router(waitlist_router)


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return success_response(
        data={"status": "ok"},
        message="healthy"
    )
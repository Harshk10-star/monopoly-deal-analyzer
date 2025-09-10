from fastapi import APIRouter
from app.api.v1.endpoints import auth, analysis, payments, users, configuration

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["game analysis"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(configuration.router, prefix="/configuration", tags=["configuration"])


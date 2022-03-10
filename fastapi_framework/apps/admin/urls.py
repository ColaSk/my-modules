from fastapi import APIRouter
from .views import router

api_router = APIRouter()

api_router.include_router(router, prefix='/admin')
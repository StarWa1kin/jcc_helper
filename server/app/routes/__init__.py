from fastapi import APIRouter

from app.routes import base, equips, gods, heroes, hexes, traits

api_router = APIRouter()
api_router.include_router(base.router)
api_router.include_router(heroes.router)
api_router.include_router(traits.router)
api_router.include_router(hexes.router)
api_router.include_router(gods.router)
api_router.include_router(equips.router)

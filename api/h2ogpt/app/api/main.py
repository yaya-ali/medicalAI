from fastapi import APIRouter
from h2ogpt.app.api.routes import doc, h2ogpt

api_router = APIRouter()

api_router.include_router(doc.router, prefix="/doc", tags=["doc"])
api_router.include_router(h2ogpt.router, prefix="/h2ogpt", tags=["h2ogpt"])

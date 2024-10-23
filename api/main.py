from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference

from db.api.main import api_router as db_router
from db.pipeline.utils.exception_handler import (
    ExceptionHandler as pipeline_exception_handler,
)
from medpub.doaj.api.main import api_router as medpub_doaj_router
from h2ogpt.app.api.main import api_router as h2ogpt_router
from h2ogpt.app.core.utils.exceptions import (
    ExceptionHandler as h2ogpt_exception_handler,
)
from auth.src.api.main import api_router as auth_router
from auth.src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_VERSION_PREFIX}/openapi.json",
    docs_url=f"{settings.API_VERSION_PREFIX}/docs",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get(f"{settings.API_VERSION_PREFIX}/scalar", include_in_schema=False)
async def scalar():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, title=settings.PROJECT_NAME  # type: ignore
    )


# internal server error handler
@app.exception_handler(Exception)
async def custom_http_exception_handler(_, exc):
    if isinstance(exc, (pipeline_exception_handler, h2ogpt_exception_handler)):
        return JSONResponse(status_code=500, content=exc.__repr__())
    return JSONResponse(status_code=500, content={"msg": exc.__str__()})


app.include_router(auth_router, prefix=settings.API_VERSION_PREFIX)
# app.include_router(medpub_doaj_router, prefix=settings.API_VERSION_PREFIX)
app.include_router(db_router, prefix=settings.API_VERSION_PREFIX)
app.include_router(h2ogpt_router, prefix=settings.API_VERSION_PREFIX)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import hr
from .utils.logging import configure_logging

settings = get_settings()
configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# CORS (adapt for enterprise)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # enterprise can restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(hr.router, prefix="/api/v1/hr", tags=["HR Assistant"])


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "env": settings.ENVIRONMENT}

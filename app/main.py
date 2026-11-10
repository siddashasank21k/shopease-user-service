import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.database.connection import engine, Base
from app.models.user_model import UserProfile
from app.models.address_model import UserAddress
from app.routers import user_routes, address_routes

logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    connected = False
    for attempt in range(1, 16):
        try:
            logger.info(f"Connecting to MySQL database (attempt {attempt}/15)...")
            Base.metadata.create_all(bind=engine)
            logger.info("User database connected and tables initialized.")
            connected = True
            break
        except Exception as e:
            logger.warning(f"Database handshake pending: {e}. Retrying in 2 seconds...")
            time.sleep(2)
    yield

app = FastAPI(
    title=settings.APP_NAME,
    description="Dedicated microservice handling customer profiles, addresses, and account operations.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(user_routes.router)
app.include_router(address_routes.router)

@app.get("/health", tags=["Health"])
def health():
    return JSONResponse(status_code=200, content={"status": "healthy", "service": settings.APP_NAME})

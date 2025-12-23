from contextlib import asynccontextmanager
from api.raybatch import rayRosteringRouter
from config.logger import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import ALLOWED_ORIGINS



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("lifespan invoked")

#app = FastAPI(lifespan=lifespan)
app = FastAPI()
@app.middleware("http")
async def log_origin(request, call_next):
    origin = request.headers.get("origin")
    logger.info(f"Request from origin: {origin}")
    logger.info(f"FASTAPI --> {request.method} {request.url.path}")

    return await call_next(request)

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS or ["*"],  # use from config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(rayRosteringRouter, prefix="/ray")
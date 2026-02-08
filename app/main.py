from fastapi import FastAPI
from app.routes.sr_webhook import router as sr_router
from app.routes.raw_webhook import router as raw_router
from app.routes.dashboard import router as dashboard_router

app = FastAPI()

app.include_router(dashboard_router)
app.include_router(sr_router)
app.include_router(raw_router)

from fastapi import FastAPI
from app.routes.sr_webhook import router as sr_router
from app.routes.raw_webhook import router as raw_router
from app.routes.dashboard import router as dashboard_router
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.daily_summary import send_final_support_summary

app = FastAPI()

app.include_router(dashboard_router)
app.include_router(sr_router)
app.include_router(raw_router)

scheduler = BackgroundScheduler()
scheduler.add_job(
    send_final_support_summary,
    trigger='cron',
    hour=15,
    minute=5
)
scheduler.start()

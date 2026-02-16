from fastapi import FastAPI
from app.routes.dashboard import router as dashboard_router
from app.routes.dynamic_webhook import router as dynamic_router  # ✅ ADD THIS
from app.routes.dispatch_webhook import router as dispatch_router  # ✅ ADD THIS
app = FastAPI()

# ✅ Register routers
app.include_router(dispatch_router)
app.include_router(dashboard_router)
app.include_router(dynamic_router)  # ✅ ADD THIS LINE

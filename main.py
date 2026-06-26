from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from backend.routes import router
from backend.scheduler import start_scheduler

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting Website Monitoring Scheduler...")

    start_scheduler()

    yield

    print("Application Shutdown")


app = FastAPI(
    title="Website Uptime Monitor",
    lifespan=lifespan
)

app.mount("/style", StaticFiles(directory="Frontend/style"), name="style")

app.include_router(router)

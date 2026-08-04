from routers import tasks
from fastapi import FastAPI


app = FastAPI()


app.include_router(tasks.router)
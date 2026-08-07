from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

# Добавили auth вот сюда:
from routers import tasks, auth 
from database import AsyncSessionLocal
from models import Task

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(tasks.router)
# И подключили роутер вот сюда:
app.include_router(auth.router)  

# ... дальше твой tasks_page остается как был

@app.get("/ui/tasks")
async def tasks_page(request: Request):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Task))
        real_tasks = result.scalars().all()
    
    return templates.TemplateResponse(
        request=request,
        name="tasks.html", 
        context={"tasks": real_tasks}
    )
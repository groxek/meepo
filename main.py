from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from routers import tasks, auth 
from database import AsyncSessionLocal
from models import Task

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(tasks.router)
app.include_router(auth.router)  


@app.get("/", response_class=HTMLResponse)
async def tasks_page(request: Request):
    async with AsyncSessionLocal() as session:
        stmt = select(Task).options(joinedload(Task.subject))
        result = await session.execute(stmt)
        real_tasks = result.scalars().unique().all()
    
    return templates.TemplateResponse(
        request=request,
        name="tasks.html", 
        context={"tasks": real_tasks}
    )
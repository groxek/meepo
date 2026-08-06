from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from routers import tasks
from database import engine, Base
import models

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(tasks.router)


@app.get("/ui/tasks")
async def tasks_page(request: Request):
    mock_tasks_from_db = [
        {
            "id": 1,
            "subject": "Algebra",
            "title": "Quadratic Systems",
            "description": "Solve systems of quadratic equations.",
            "difficulty": "Beginner",
            "color": "purple",
            "dot_color": "emerald"
        },
        {
            "id": 2,
            "subject": "Geometry",
            "title": "Circle Theorems",
            "description": "Apply inscribed angle theorems.",
            "difficulty": "Advanced",
            "color": "orange",
            "dot_color": "red"
        }
    ]
    
    return templates.TemplateResponse(
        request=request,
        name="tasks.html", 
        context={"tasks": mock_tasks_from_db}
    )
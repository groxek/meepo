from fastapi import APIRouter
from sqlalchemy import select
from sqlalchemy.sql.expression import func
from database import AsyncSessionLocal
from models import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
async def get_tasks():
    return {"message": "wasssapp"}

@router.get("/random")
async def get_random_task():
    async with AsyncSessionLocal() as session:
        stmt = select(Task).order_by(func.random()).limit(1)
        
        result = await session.execute(stmt)
        random_task = result.scalar_one_or_none()
        
        if not random_task:
            return {"error": "База задач пуста"}
            
        return {
            "id": random_task.id,
            "subject_id": random_task.subject_id,
            "question": random_task.question,
            "answer": random_task.answer
        }
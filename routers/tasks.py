from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from models import Task, User, Attempt
from dependencies import get_current_user, get_db
from schemas import UserAnswer, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
async def get_tasks():
    return {"message": "yoo"}

@router.get("/random", response_model=TaskResponse)
async def get_random_task(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    stmt = select(Task).order_by(func.random()).limit(1)
    result = await session.execute(stmt)
    random_task = result.scalar_one_or_none()
    
    if not random_task:
        raise HTTPException(status_code=404, detail="База задач пуста")
        
    return random_task

@router.post("/{task_id}/attempt")
async def submit_attempt(
    task_id: int, 
    user_answer: UserAnswer, 
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    query = select(Task).where(Task.id == task_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    correct_ans = str(task.answer).strip().replace(',', '.').lower()
    user_ans = str(user_answer.answer).strip().replace(',', '.').lower()

    is_correct = (correct_ans == user_ans)

    new_attempt = Attempt(
        user_id=current_user.id,
        task_id=task.id,
        user_input=user_answer.answer,
        is_correct=is_correct
    )
    session.add(new_attempt)
    await session.commit()

    return {
        "task_id": task.id,
        "user_input": user_answer.answer,
        "is_correct": is_correct,
        "message": "Есть же!" if is_correct else "Неправильно, пробуй еще раз."
    }
import asyncio
from sqlalchemy import select
from database import AsyncSessionLocal
from models import Subject, Task

async def seed_db():
    async with AsyncSessionLocal() as session:
        
        await session.execute(Task.__table__.delete())
        await session.execute(Subject.__table__.delete())
        await session.commit()
        print("База очищена.")

        print("Создаем предметы...")
        math = Subject(name="Профильная Математика")
        inf = Subject(name="Информатика")
        
        session.add_all([math, inf])
        await session.flush() 

        print("Создаем задачи...")
        task1 = Task(
            subject_id=math.id, 
            question="Решите уравнение: x^2 - 4 = 0. В ответ запишите больший корень.", 
            answer="2"
        )
        task2 = Task(
            subject_id=inf.id, 
            question="Сколько единиц содержит двоичная запись числа 1023?", 
            answer="10"
        )
        
        session.add_all([task1, task2])
        await session.commit()
        print("Успех! Данные записаны.\n")

        print("--- ЧИТАЕМ ИЗ БАЗЫ ---")
        tasks_from_db = await session.execute(select(Task))
        
        for t in tasks_from_db.scalars():
            print(f"ID {t.id} | Предмет ID: {t.subject_id} | Вопрос: {t.question} | Ответ: {t.answer}")

if __name__ == "__main__":
    asyncio.run(seed_db())
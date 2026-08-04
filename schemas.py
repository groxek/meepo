from pydantic import BaseModel





class UserBase(BaseModel):
    username: str

class SubjectBase(BaseModel):
    name: str

class TaskBase(BaseModel):
    subject_id: int
    question: str

class AttemptBase(BaseModel):
    user_id: int
    task_id: int
    user_input: str





class UserCreate(UserBase):
    password: str
    pass

class SubjectCreate(SubjectBase):
    pass

class TaskCreate(TaskBase):
    answer: str | int
    pass

class AttemptCreate(AttemptBase):
    pass





class User(UserBase):
    id: int

class Subject(SubjectBase):
    id: int

class Task(TaskBase):
    id: int

class Attempt(AttemptBase):
    id: int
    is_correct: bool
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str

class SubjectBase(BaseModel):
    name: str

class TaskBase(BaseModel):
    subject_id: int
    question: str
    images: list[str] = Field(default_factory=list)
    ege_number: int | None = None

class AttemptBase(BaseModel):
    user_id: int
    task_id: int
    user_input: str


class UserCreate(UserBase):
    password: str = Field(min_length=8)

class SubjectCreate(SubjectBase):
    pass

class TaskCreate(TaskBase):
    answer: str | int

class AttemptCreate(AttemptBase):
    pass


class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class SubjectResponse(SubjectBase):
    id: int
    
    class Config:
        from_attributes = True

class TaskResponse(TaskBase):
    id: int
    
    class Config:
        from_attributes = True

class AttemptResponse(AttemptBase):
    id: int
    is_correct: bool
    
    class Config:
        from_attributes = True



class UserAnswer(BaseModel):
    answer: str
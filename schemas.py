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
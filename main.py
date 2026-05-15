from datetime import datetime
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

import database
from auth import authenticate_user, create_access_token, get_current_user
from models import Task, TaskCreate, Token, UserInDB

app = FastAPI(title="Task Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "task_count": len(database.tasks_db)}


@app.post("/auth/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.username})
    return Token(access_token=token, token_type="bearer")


@app.get("/tasks", response_model=list[Task])
def get_tasks(current_user: UserInDB = Depends(get_current_user)):
    return [
        task
        for task in database.tasks_db.values()
        if task.owner_username == current_user.username
    ]


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    current_user: UserInDB = Depends(get_current_user),
):
    task = Task(
        id=uuid4(),
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        created_at=datetime.utcnow(),
        owner_username=current_user.username,
    )
    database.tasks_db[str(task.id)] = task
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    if task_id not in database.tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    del database.tasks_db[task_id]

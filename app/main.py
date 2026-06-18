from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import TaskDB
from .schemas import TaskCreate, TaskResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevOps Task Manager",
    description="Mini-projet DevOps niveau Master 2",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to DevOps Task Manager"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskDB).all()

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    existing_task = db.query(TaskDB).filter(TaskDB.id == task.id).first()

    if existing_task:
        raise HTTPException(status_code=400, detail="Task already exists")

    new_task = TaskDB(
        id=task.id,
        title=task.title,
        completed=task.completed
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}
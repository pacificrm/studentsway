from fastapi import APIRouter, HTTPException, Depends, status, Form
from fastapi import APIRouter, HTTPException, Depends, status as http_status, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import Date, Time, Integer, String, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from service.core.logic.init_db import SessionLocal
from service.core.schemas.models import Student,Task
from datetime import datetime
from service.core.logic.init_db import SessionLocal


Base = declarative_base()

task_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET tasks by student email
@task_router.get("/task/{email}")
async def get_tasks_by_email(email: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    tasks = db.query(Task).filter(Task.student_id == email).all()
    
    if not tasks:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="No tasks found for the student")

    # Prepare the tasks to be JSON serializable
    tasks_data = [
        {
            "id": task.id,
            "task_name": task.task_name,
            "task_date": task.task_date.isoformat(),
            "task_time": task.task_time.isoformat(),
            "task_deadline": task.task_deadline.isoformat(),
            "status": task.status,
        }
        for task in tasks
    ]
    
    return JSONResponse(content=tasks_data, status_code=http_status.HTTP_200_OK)


# POST a new task by student email (using form data)@task_router.post("/task/{email}")
# task_router = APIRouter()

@task_router.post("/task/{email}")
async def add_task_by_email(
    email: str,
    task_name: str = Form(...),
    task_date: str = Form(...),
    task_time: str = Form(...),
    task_deadline: str = Form(...),
    task_status: str = Form(...), 
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    try:
        task_date_obj = datetime.strptime(task_date, "%Y-%m-%d").date()
        task_time_obj = datetime.strptime(task_time, "%H:%M").time()
        task_deadline_obj = datetime.strptime(task_deadline, "%Y-%m-%d").date()
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid date/time format: {str(e)}")
    
    new_task = Task(
        task_name=task_name,
        task_date=task_date_obj,
        task_time=task_time_obj,
        task_deadline=task_deadline_obj,
        status=task_status, 
        student_id=student.email  
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return JSONResponse(content={"message": "Task created successfully", "task": new_task.id}, status_code=status.HTTP_201_CREATED)


# New endpoint to mark a task as complete
@task_router.patch("/task/markcomplete/{id}")
async def mark_task_complete(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    task.status = "completed" 
    db.commit()
    db.refresh(task)
    
    return JSONResponse(content={"message": "Task marked as complete", "task": task.id}, status_code=status.HTTP_200_OK)
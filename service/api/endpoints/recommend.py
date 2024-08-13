from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from service.core.schemas.models import Parent, Teacher, School, Student, Playground
from service.core.logic.init_db import SessionLocal

# Routers
reco_parent_router = APIRouter()
reco_teacher_router = APIRouter()
reco_student_router = APIRouter()
reco_ground_router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Recommend teachers to parents based on the same cluster
@reco_parent_router.get("/recommend/parent/{email}")
async def recommend_teachers_to_parent(email: str, db: Session = Depends(get_db)):
    parent = db.query(Parent).filter(Parent.email == email).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    teachers = db.query(Teacher).filter(Teacher.cluster == parent.cluster).all()
    return [{"name": teacher.name, "email": teacher.email, "address": teacher.address} for teacher in teachers]

# Recommend parents to teachers based on the same cluster
@reco_teacher_router.get("/recommend/teacher/{email}")
async def recommend_parents_to_teacher(email: str, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.email == email).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    parents = db.query(Parent).filter(Parent.cluster == teacher.cluster).all()
    return [{"name": parent.name, "email": parent.email, "address": parent.address} for parent in parents]

# Recommend grounds to students based on the same cluster
@reco_ground_router.get("/recommend/ground/{email}")
async def recommend_grounds_to_student(email: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    grounds = db.query(Playground).filter(Playground.cluster == student.cluster).all()
    return [{"groundid": ground.groundid, "name": ground.name, "address": ground.address} for ground in grounds]

# Recommend students to a student based on the same cluster, sorted by school and class
@reco_student_router.get("/recommend/student/{email}")
async def recommend_students_to_student(email: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    students = db.query(Student).filter(Student.cluster == student.cluster).order_by(
        Student.school_id, Student.class_name
    ).all()
    return [
        {
            "name": s.name,
            "class_name": s.class_name,
            "email": s.email,
            "address": s.address,
            "school_id": s.school_id,
        }
        for s in students
    ]
from fastapi import APIRouter, UploadFile, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from service.core.schemas.models import Teacher
from service.core.logic.init_db import SessionLocal

teacher_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@teacher_router.post("/addteacher")
async def add_teacher(
    email: str = Form(...),
    name: str = Form(...),
    school_name: str = Form(...),
    address: str = Form(...),
    password: str = Form(None),
    db: Session = Depends(get_db)
):
    # Determine the cluster based on the address
    cluster = 2 if "pachimvihar" in address.lower() else 1
    
    # Create a new teacher record
    new_teacher = Teacher(
        email=email,
        name=name,
        school_id=school_name,
        address=address,
        password=password,
        cluster=cluster,
        profile_pic=None,  # Assuming profile_pic is not provided at this point
        role="teacher"  # Setting role to 'teacher'
    )
    
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    
    return JSONResponse(content={"message": "Teacher added successfully", "teacher": new_teacher.email}, status_code=201)

@teacher_router.get("/teacher/{email}")
async def get_teacher(email: str, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.email == email).first()
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    school_name = teacher.school.name if teacher.school else teacher.school_id
    
    return {
        "name": teacher.name,
        "address": teacher.address,
        "school_name": school_name
    }

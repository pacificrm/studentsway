from fastapi import APIRouter, UploadFile, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from service.core.schemas.models import Parent,Student
from service.core.logic.init_db import SessionLocal

parent_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@parent_router.post("/addparent")
async def add_parent(
    email: str = Form(...),
    name: str = Form(...),
    address: str = Form(...),
    password: str = Form(None),
    db: Session = Depends(get_db)
):
    # Determine the cluster based on the address
    cluster = 2 if "pachimvihar" in address.lower() else 1
    
    # Create a new parent record
    new_parent = Parent(
        email=email,
        name=name,
        address=address,
        password=password,
        cluster=cluster,
        profile_pic=None,  # Assuming profile_pic is not provided at this point
        role="parent"  # Setting role to 'parent'
    )
    
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)
    
    return JSONResponse(content={"message": "Parent added successfully", "parent": new_parent.email}, status_code=201)

@parent_router.get("/parent/{email}")
async def get_parent(email: str, db: Session = Depends(get_db)):
    parent = db.query(Parent).filter(Parent.email == email).first()
    
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    # Extract student details
    students_info = [
        {"email": student.email, "name": student.name, "class": student.class_name}
        for student in parent.students
    ]
    
    return {
        "name": parent.name,
        "address": parent.address,
        "students": students_info
    }

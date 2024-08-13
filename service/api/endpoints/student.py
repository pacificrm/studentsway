from fastapi import APIRouter, UploadFile, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO
import numpy as np
from sqlalchemy.orm import Session
from service.core.logic.OCR import extract_text_from_image
from service.core.schemas.models import Student, Parent,School
from service.core.schemas.output import APIOutput
from service.core.logic.init_db import SessionLocal

student_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Merged POST for student validation and addition
@student_router.post("/addstudent/{emailid}")
async def validate_and_add_student(
    emailid: str,
    id: UploadFile,
    name: str = Form(...),
    email : str=Form(...),
    father_name: str = Form(...),
    school_name: str = Form(...),
    address: str = Form(...),
    class_name: str = Form(...),
    db: Session = Depends(get_db)
):
    # Validate the image file
    if id.filename.split(".")[-1] not in ("jpg", "jpeg", "png"):
        raise HTTPException(status_code=415, detail="Not an image")

    image = Image.open(BytesIO(await id.read()))
    image = image.resize((1024, 1024))
    image = np.array(image)

    extracted_text = extract_text_from_image(image)
    
    # Validate extracted text against provided details
    provided_data = {
        "Student Name": name,
        "Father's Name": father_name,
        "School Name": school_name,  
        "Address": address,
        "Class": class_name,
        "email" : email
    }

    matches = 0
    if extracted_text.get('Student Name') in provided_data['Student Name'] and extracted_text['Student Name']:
        matches += 1
    if extracted_text.get("Father's Name") in provided_data["Father's Name"] and extracted_text["Father's Name"]:
        matches += 1
    if extracted_text.get("School Name") in str(provided_data["School Name"]) and extracted_text["School Name"]:
        matches += 1
    if extracted_text.get("Address") in provided_data["Address"] and extracted_text["Address"]:
        matches += 1
    if extracted_text.get("Class") in provided_data["Class"] and extracted_text["Class"]:
        matches += 1

    if matches < 1:
        raise HTTPException(status_code=422, detail="Validation failed, insufficient matches.")

    # If validation passes, add the student
    parent = db.query(Parent).filter(Parent.email == emailid).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    # Determine the cluster based on the address
    cluster = 2 if "pachimvihar" in address.lower() else 1
    
    # Create a new student record
    new_student = Student(
        email=email,
        name=name,
        school_id=school_name,
        class_name=class_name,
        address=address,
        cluster=cluster,
        password=None,  # Password is kept null
        fathers_name=father_name,
        profile_pic=None,  # Assuming profile_pic is not provided at this point
        role="student",  # Setting role to 'student'
        parent_id=emailid  # Assuming Parent model has an 'id' primary key field
    )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    
    return JSONResponse(content={"message": "Student added successfully", "student": new_student.email}, status_code=201)


@student_router.get("/student/{email}")
async def get_student_info(email: str, db: Session = Depends(get_db)):
    # Fetch the student based on email
    student = db.query(Student).filter(Student.email == email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch the school based on school_id
    school = db.query(School).filter(School.schoolid == student.school_id).first()
    school_name = school.name if school else student.school_id

    # Construct the response data
    student_info = {
        "name": student.name,
        "address": student.address,
        "class_name": student.class_name,
        "school_name": school_name
    }

    return student_info
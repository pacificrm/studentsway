from fastapi import APIRouter, UploadFile, HTTPException, Form
from PIL import Image
from io import BytesIO
import numpy as np
from service.core.logic.OCR import extract_text_from_image
from service.core.schemas.output import APIOutput

detect_router = APIRouter()

@detect_router.post("/studentValidation", response_model=APIOutput)
async def detect(
    id: UploadFile,
    name: str = Form(...),
    father_name: str = Form(...),
    school: str = Form(...),
    address: str = Form(...),
    class_name: str = Form(...)
):
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
        "School Name": school,
        "Address": address,
        "Class": class_name
    }

    print(provided_data)
    print(extracted_text)
    matches=0
    if extracted_text['Student Name'] in provided_data['Student Name'] and extracted_text['Student Name'] != "":
        matches += 1
    if extracted_text["Father's Name"] in provided_data["Father's Name"] and extracted_text["Father's Name"] != "":
        matches += 1
    if extracted_text["School Name"] in provided_data["School Name"] and extracted_text["School Name"] != "":
        matches += 1
    if extracted_text["Address"] in provided_data["Address"] and extracted_text["Address"] != "":
        matches += 1
    if extracted_text["Class"] in provided_data["Class"] and extracted_text["Class"] != "":
        matches += 1

 
    print(matches)
    
    if matches >= 2:
        return APIOutput(status= "validate")
        
    else:
        return APIOutput(status= "not-validate")

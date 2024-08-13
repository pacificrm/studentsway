from fastapi import APIRouter, UploadFile, HTTPException
from PIL import Image
from io import BytesIO
import numpy as np
import easyocr
from transformers import pipeline
import textwrap

summary_router = APIRouter()

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

@summary_router.post("/summarize")
async def summarize_image(im: UploadFile):
    try:
        # Read the image file
        image = Image.open(BytesIO(await im.read()))
        
        # Convert image to numpy array
        image_np = np.array(image)
        
        # Perform OCR on the image
        results = reader.readtext(image_np)
        
        # Extract text from OCR results
        text = " ".join([result[1] for result in results])
        
        if not text:
            raise HTTPException(status_code=400, detail="No text found in the image")
        
        # Summarize the extracted text
        summary = summarizer(text, max_length=350, min_length=30, do_sample=False)
        
        return {"summary": summary[0]['summary_text']}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
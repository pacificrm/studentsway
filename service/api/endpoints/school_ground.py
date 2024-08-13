from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from service.core.schemas.models import School, Playground
from service.core.logic.init_db import SessionLocal

school_router = APIRouter()
ground_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@school_router.get("/school/{school_id}")
async def get_school_info(school_id: str, db: Session = Depends(get_db)):
    school = db.query(School).filter(School.schoolid == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return {
        "schoolid": school.schoolid,
        "name": school.name,
        "address": school.address
    }

@ground_router.get("/ground/{ground_id}")
async def get_ground_info(ground_id: str, db: Session = Depends(get_db)):
    ground = db.query(Playground).filter(Playground.groundid == ground_id).first()
    if not ground:
        raise HTTPException(status_code=404, detail="Ground not found")
    return {
        "groundid": ground.groundid,
        "name": ground.name,
        "address": ground.address
    }
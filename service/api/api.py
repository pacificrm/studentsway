from fastapi import APIRouter, UploadFile,HTTPException
from service.api.endpoints.detect import detect_router
# from service.api.endpoints.test import test_router
from service.api.endpoints.summarize import summary_router
from service.api.endpoints.school_ground import ground_router,school_router
from service.api.endpoints.recommend import reco_ground_router,reco_parent_router,reco_student_router,reco_teacher_router
from service.api.endpoints.tasks import task_router
from service.api.endpoints.student import student_router
from service.api.endpoints.teacher import teacher_router
from service.api.endpoints.parent import parent_router

main_router=APIRouter()

main_router.include_router(detect_router)
main_router.include_router(summary_router)
main_router.include_router(ground_router)
main_router.include_router(school_router)
main_router.include_router(reco_teacher_router)
main_router.include_router(reco_ground_router)
main_router.include_router(reco_parent_router)
main_router.include_router(reco_student_router)
main_router.include_router(task_router)
main_router.include_router(student_router)
main_router.include_router(parent_router)
main_router.include_router(teacher_router)

# main_router.include_router(test_router)

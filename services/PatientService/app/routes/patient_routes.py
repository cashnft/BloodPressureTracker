
from fastapi import APIRouter, Depends
from app.services.patient_service import PatientService
from app.utils.feature_toggle import feature_toggle


from app.cache import cache  

router = APIRouter()

def get_patient_service():
    return PatientService(cache)

@router.get("/patients/{ssn}")
@feature_toggle("patient_read")
async def get_patient(ssn: str, service: PatientService = Depends(get_patient_service)):
    return await service.get_patient(ssn)
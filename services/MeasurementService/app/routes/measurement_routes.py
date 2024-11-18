from fastapi import APIRouter, Depends
from app.services.measurement_service import MeasurementService
from app.models import Measurement, MeasurementCreate
from app.cache import cache
from app.utils.feature_toggle import feature_toggle

router = APIRouter()

def get_measurement_service():
    return MeasurementService(cache)

@router.get("/measurements/{patient_ssn}")
@feature_toggle("measurement_read")
async def get_measurements(
    patient_ssn: str, 
    service: MeasurementService = Depends(get_measurement_service)
):
    return await service.get_measurements(patient_ssn)

@router.post("/measurements")
@feature_toggle("measurement_write")
async def create_measurement(
    measurement: MeasurementCreate,
    service: MeasurementService = Depends(get_measurement_service)
):
    return await service.create_measurement(measurement)
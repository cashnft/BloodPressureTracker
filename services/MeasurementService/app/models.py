from pydantic import BaseModel
from datetime import datetime

class MeasurementBase(BaseModel):
    patient_ssn: str
    systolic: int
    diastolic: int
    timestamp: datetime = datetime.now()

class MeasurementCreate(MeasurementBase):
    pass

class Measurement(MeasurementBase):
    id: int

    class Config:
        from_attributes = True
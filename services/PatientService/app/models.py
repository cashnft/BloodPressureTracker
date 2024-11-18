from datetime import datetime
from pydantic import BaseModel, EmailStr

class Patient(BaseModel):
    ssn: str
    name: str
    email: EmailStr

class PatientInDB(Patient):
    created_at: datetime
    updated_at: datetime
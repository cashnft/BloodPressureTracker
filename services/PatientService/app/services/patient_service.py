from app.models import Patient
from app.database import db

from app.utils.circuit_breaker import CircuitBreaker
from app.utils.rate_limiter import rate_limit

class PatientService:
    def __init__(self, cache_instance):
        self.cache = cache_instance
    @CircuitBreaker()
    @rate_limit(limit=100, window=60)
    async def get_patient(self, ssn: str) -> Patient:
   
        cached = await self.cache.get(f"patient:{ssn}")
        if cached:
            return Patient(**cached)

        async with db.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT * FROM patients WHERE ssn = %s",
                    (ssn,)
                )
                result = await cur.fetchone()
                if not result:
                    return None
                
                patient = Patient(
                    ssn=result[0],
                    name=result[1],
                    email=result[2]
                )
                
                #caching the result
                await self.cache.set(f"patient:{ssn}", patient.dict())
                return patient
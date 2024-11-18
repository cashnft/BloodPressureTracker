from app.models import Measurement, MeasurementCreate
from app.utils.circuit_breaker import CircuitBreaker
from app.utils.rate_limiter import rate_limit
from fastapi import HTTPException

class MeasurementService:
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @CircuitBreaker()
    @rate_limit(limit=100, window=60)
    async def get_measurements(self, patient_ssn: str) -> list[Measurement]:
  
        cached = await self.cache.get(f"measurements:{patient_ssn}")
        if cached:
            return [Measurement(**m) for m in cached]

        async with self.db.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """SELECT id, patient_ssn, systolic, diastolic, timestamp 
                       FROM measurements 
                       WHERE patient_ssn = %s 
                       ORDER BY timestamp DESC""",
                    (patient_ssn,)
                )
                result = await cur.fetchall()
                
                measurements = [
                    Measurement(
                        id=row[0],
                        patient_ssn=row[1],
                        systolic=row[2],
                        diastolic=row[3],
                        timestamp=row[4]
                    ) for row in result
                ]
                
                if measurements:
                    await self.cache.set(f"measurements:{patient_ssn}", 
                                       [m.dict() for m in measurements])
                return measurements

    @CircuitBreaker()
    @rate_limit(limit=50, window=60)
    async def create_measurement(self, measurement: MeasurementCreate) -> Measurement:
        async with self.db.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """INSERT INTO measurements 
                       (patient_ssn, systolic, diastolic, timestamp)
                       VALUES (%s, %s, %s, %s)""",
                    (measurement.patient_ssn, measurement.systolic,
                     measurement.diastolic, measurement.timestamp)
                )
                await cur.execute("SELECT LAST_INSERT_ID()")
                measurement_id = (await cur.fetchone())[0]
                
   
                await self.cache.delete(f"measurements:{measurement.patient_ssn}")
                
                return Measurement(id=measurement_id, **measurement.dict())
import pytest
from unittest.mock import AsyncMock, patch
from app.services.patient_service import PatientService
from app.models import Patient
from app.utils.circuit_breaker import CircuitBreaker
from fastapi import HTTPException

@pytest.mark.asyncio
class TestPatientService:
   @pytest.fixture
   async def service(self):
       return PatientService()

   @pytest.fixture
   def mock_patient(self):
       return Patient(
           ssn="123456789",
           name="Test Patient",
           email="test@example.com"
       )

   async def test_get_patient_success(self, service, mock_patient):
       
       with patch('app.cache.Cache.get', return_value=AsyncMock(return_value=None)):
           
           with patch('app.database.Database.connection') as mock_conn:
               mock_cursor = AsyncMock()
               mock_cursor.fetchone.return_value = (
                   mock_patient.ssn,
                   mock_patient.name,
                   mock_patient.email
               )
               mock_conn.return_value.__aenter__.return_value.cursor.return_value.__aenter__.return_value = mock_cursor
               
               result = await service.get_patient(mock_patient.ssn)
               assert result.ssn == mock_patient.ssn
               assert result.name == mock_patient.name

   async def test_get_patient_cached(self, service, mock_patient):
       with patch('app.cache.Cache.get', return_value=AsyncMock(return_value=mock_patient.dict())):
           result = await service.get_patient(mock_patient.ssn)
           assert result.ssn == mock_patient.ssn

   async def test_get_patient_not_found(self, service):
       with patch('app.cache.Cache.get', return_value=AsyncMock(return_value=None)):
           with patch('app.database.Database.connection') as mock_conn:
               mock_cursor = AsyncMock()
               mock_cursor.fetchone.return_value = None
               mock_conn.return_value.__aenter__.return_value.cursor.return_value.__aenter__.return_value = mock_cursor
               
               with pytest.raises(HTTPException) as exc:
                   await service.get_patient("nonexistent")
               assert exc.value.status_code == 404

   async def test_rate_limiter(self, service):
       with patch('app.utils.rate_limiter.RateLimiter.is_rate_limited', 
                 return_value=AsyncMock(return_value=True)):
           with pytest.raises(HTTPException) as exc:
               await service.get_patient("123")
           assert exc.value.status_code == 429

   async def test_circuit_breaker(self, service):
       circuit_breaker = CircuitBreaker(failure_threshold=2, recovery_time=1)
       
   
       for _ in range(3):
           with pytest.raises(Exception):
               await circuit_breaker(lambda: AsyncMock(side_effect=Exception()))()
       with pytest.raises(HTTPException) as exc:
           await circuit_breaker(lambda: AsyncMock())()
       assert exc.value.status_code == 503
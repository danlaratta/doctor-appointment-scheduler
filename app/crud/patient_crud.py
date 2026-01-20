from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.patient import Patient
from app.exceptions.database_exception import DatabaseException

class PatientCrud:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
    
    # Create Patient
    async def create_patient(self, patient: Patient) -> Patient:
        self.db_session.add(patient)

        try:
            await self.db_session.commit()
            await self.db_session.refresh(patient)
        except IntegrityError as e:
            await self.db_session.rollback()
            raise DatabaseException(f'Failed to create new patient: violation of model constraints: {e}') from e
        return patient


    # Get Patient 
    async def get_patient(self, patient_id: int) -> Patient:
        result = await self.db_session.execute(select(Patient).where(Patient.id == patient_id))
        patient: Patient | None = result.scalar_one_or_none()

        if patient is None:
            raise DatabaseException(f'No patient found with id: {patient_id}')
        return patient
    

    # Check if patient exists
    async def check_patient_exists(self, patient_email: str) -> bool:
        result = await self.db_session.execute(select(Patient).where(Patient.email == patient_email))
        patient: Patient | None = result.scalar_one_or_none()

        if patient is None:
            return False
        return True 


    # Delete Patient
    async def delete_patient(self, patient_id: int) -> None:
        patient: Patient = await self.get_patient(patient_id)
        try:
            await self.db_session.delete(patient)
            await self.db_session.commit()
        except IntegrityError as e:
            await self.db_session.rollback()
            raise DatabaseException(f'Failed to delete patient: violation of model constraints: {e}') from e 

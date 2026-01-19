from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.patient import Patient
from app.exceptions.database_exception import DatabaseException

class patientCrud:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
    
    # Create Patient
    async def create_patient(self, patient_id: int) -> Patient:
        result = await self.db_session.execute(select(Patient).where(Patient.id == patient_id))
        patient: Patient | None = result.scalar_one_or_none()

        if patient is None:
            raise DatabaseException(f'No patient found patient_id with id: {patient_id}')
        return patient


    # Get Patient
    async def get_patient(self, patient_id: int) -> None:
        pass


    # Update Patient
    async def update_patient(self) -> None:
        pass


    # Delete Patient
    async def cancel_patient(self) -> None:
        pass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.doctor import Doctor
from app.exceptions.database_exception import DatabaseException

class DoctorCrud:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
    
    # Create doctor
    async def create_doctor(self, doctor_id: int) -> None:
        pass


    # Get Doctor
    async def get_doctor(self, doctor_id: int) -> Doctor:
        result = await self.db_session.execute(select(Doctor).where(Doctor.id == doctor_id))
        doctor: Doctor | None = result.scalar_one_or_none()

        if doctor is None:
            raise DatabaseException(f'No doctor found doctor_id with id: {doctor_id}')
        return doctor


    # Update Doctor
    async def update_doctor(self) -> None:
        pass


    # Delete Doctor
    async def cancel_doctor(self) -> None:
        pass


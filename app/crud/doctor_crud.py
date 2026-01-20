from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.doctor import Doctor
from app.exceptions.database_exception import DatabaseException

class DoctorCrud:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
    
    # Create doctor
    async def create_doctor(self, doctor: Doctor) -> Doctor:
        self.db_session.add(doctor)

        try:
            await self.db_session.commit()
            await self.db_session.refresh(doctor)
        except IntegrityError as e:
            await self.db_session.rollback()
            raise DatabaseException(f'Failed to create new doctor: violation of model constraints: {e}') from e
        return doctor


    # Get Doctor
    async def get_doctor(self, doctor_id: int) -> Doctor:
        result = await self.db_session.execute(select(Doctor).where(Doctor.id == doctor_id))
        doctor: Doctor | None = result.scalar_one_or_none()

        if doctor is None:
            raise DatabaseException(f'No doctor found with id: {doctor_id}')
        return doctor
    

    # Check if doctor exists
    async def check_doctor_exists(self, doctor_email: str) -> bool:
        result = await self.db_session.execute(select(Doctor).where(Doctor.email == doctor_email))
        doctor: Doctor | None = result.scalar_one_or_none()

        if doctor is None:
            return False
        return True 


    # Delete Doctor
    async def delete_doctor(self, doctor_id: int) -> None:
        doctor: Doctor = await self.get_doctor(doctor_id)
        try:
            await self.db_session.delete(doctor)
            await self.db_session.commit()
        except IntegrityError as e:
            await self.db_session.rollback()
            raise DatabaseException(f'Failed to delete doctor: violation of model constraints: {e}') from e 


from datetime import time
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.doctor_schedule import DoctorSchedule
from app.exceptions.database_exception import DatabaseException

class DoctorScheduleCrud:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session


    # Create schedule
    async def create_schedule(self, schedule: DoctorSchedule) -> DoctorSchedule:
        self.db_session.add(schedule)

        try:
            await self.db_session.commit()
            await self.db_session.refresh(schedule)
        except IntegrityError as e:
            await self.db_session.rollback()
            raise DatabaseException(f'Failed to create new schedule: violation of model constraints: {e}') from e
        return schedule


    # Get schedule
    async def get_schedule(self, schedule_id: int, doctor_id: int) -> DoctorSchedule:
        result = await self.db_session.execute(select(DoctorSchedule).where(DoctorSchedule.id == schedule_id).where(DoctorSchedule.doctor_id == doctor_id))
        schedule: DoctorSchedule | None = result.scalar_one_or_none()

        if schedule is None:
            raise DatabaseException(f'No schedule found with id: {schedule_id}')
        return schedule


    # Check if schedule exists for a doctor
    async def check_schedule_exists(self, doctor_id: int) -> bool:
        result = await self.db_session.execute(select(DoctorSchedule).where(DoctorSchedule.doctor_id == doctor_id))
        schedule: DoctorSchedule | None = result.scalar_one_or_none()

        if schedule is None:
            return False 
        return True


    # Update schedule
    async def update_schedule(self, schedule: DoctorSchedule) -> DoctorSchedule:
        try:
            await self.db_session.commit()
            await self.db_session.refresh(schedule)
        except IntegrityError as e:
            await self.db_session.rollback()
            raise DatabaseException(
                f'Failed to update schedule: {e}'
            ) from e

        return schedule


    # Delete Schedule
    async def delete_schedule(self, schedule_id: int, doctor_id: int) -> None:
        schedule: DoctorSchedule = await self.get_schedule(schedule_id, doctor_id)
        try:
            await self.db_session.delete(schedule)
            await self.db_session.commit()
        except IntegrityError as e:
            await self.db_session.rollback()
            raise DatabaseException(f'Failed to delete schedule: violation of model constraints: {e}') from e 

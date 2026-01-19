from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.appointment import Appointment
from app.exceptions.database_exception import DatabaseException

class AppointmentCrud:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
    
    # Create Appointment
    async def create_appointment(self) -> None:
        pass

    # Get Doctor's Appointment - single appt by date and patient
    async def get_doctor_appointment(self, appt_date: date, appt_id: int, doctor_id: int, patient_id: int) -> Appointment:
        result = await self.db_session.execute(select(Appointment)
            .where(Appointment.id == appt_id)
            .where(Appointment.appointment_date == appt_date)
            .where(Appointment.doctor_id == doctor_id)
            .where(Appointment.patient_id == patient_id)
        )

        appointment: Appointment | None = result.scalar_one_or_none()
        
        if appointment is None:
            raise DatabaseException(f'No appointment found for id={appt_id} on {appt_date} with doctor_id={doctor_id} and patient_id={patient_id}')
        return appointment


    # Get Doctor's Appointments - all appts for the day by date
    async def get_all_doctor_appointments_for_day(self, appt_date: date, doctor_id: int) -> list[Appointment]:
        result = await self.db_session.execute(select(Appointment).where(Appointment.appointment_date == appt_date).where(Appointment.doctor_id == doctor_id))

        appointments: list[Appointment] = list(result.scalars())

        if not appointments:
            raise DatabaseException('No appointments found for doctor_id={doctor_id} on {appt_date}') 
        
        return appointments
    

    # Update Appointment
    async def update_appointment(self) -> None:
        pass


    # Cancel/Delete Appointment
    async def cancel_appointment(self) -> None:
        pass


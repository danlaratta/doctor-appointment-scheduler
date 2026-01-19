from sqlalchemy.ext.asyncio import AsyncSession

class AppointmentCrud:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session
    
    # Create Appointment
    async def create_appointment(self) -> None:
        pass
    

    # Get Doctor's Appointment - single appt by date
    async def get_doctor_appointment(self) -> None:
        pass
    

    # Get Doctor's Appointments - all appts for the day by date
    async def get_all_doctor_appointments_for_day(self) -> None:
        pass
    

    # Get Patient's Appointment - single appt
    async def get_patient_appointment(self) -> None:
        pass
    

    # Update Appointment
    async def update_appointment(self) -> None:
        pass
    

    # Cancel/Delete Appointment
    async def cancel_appointment(self) -> None:
        pass


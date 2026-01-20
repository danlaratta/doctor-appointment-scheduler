from datetime import time
from app.crud.doctor_schedule_crud import DoctorScheduleCrud
from app.crud.doctor_crud import DoctorCrud
from app.models.doctor_schedule import DoctorSchedule
from app.models.doctor import Doctor

class DoctorScheduleService:
    def __init__(self, schedule_crud: DoctorScheduleCrud, doctor_crud: DoctorCrud) -> None:
        self.schedule_crud = schedule_crud
        self.doctor_crud = doctor_crud

    
    # Create schedule for doctor
    async def create_doctor_schedule(self, doctor_id: int, weekday_start_time: time, weekday_end_time: time, weekend_start_time: time | None, weekend_end_time: time | None) -> DoctorSchedule:
        # Get doctor 
        doctor: Doctor = await self.doctor_crud.get_doctor(doctor_id)

        # Check if schedule exists for the doctor
        schedule_exists: bool = await self.schedule_crud.check_schedule_exists(doctor.id)
        if schedule_exists:
            raise ValueError('Cannot create schedule, this schedule already exists for this doctor.')
        
        # Create the schedule
        schedule: DoctorSchedule = DoctorSchedule(
            weekday_start_time = weekday_start_time,
            weekday_end_time = weekday_end_time,
            weekend_start_time = weekend_start_time,
            weekend_end_time = weekend_end_time,
            doctor_id = doctor.id
        )
        
        return await self.schedule_crud.create_schedule(schedule)
    

    # Update schedule
    async def update_doctor_schedule(self, schedule_id: int, doctor_id: int, weekday_start_time: time, weekday_end_time: time, weekend_start_time: time | None, weekend_end_time: time | None) -> DoctorSchedule:
        # Get doctor schedule
        schedule: DoctorSchedule = await self.schedule_crud.get_schedule(schedule_id, doctor_id)

        # Update the schedule
        schedule.weekday_start_time = weekday_start_time
        schedule.weekday_end_time = weekday_end_time
        schedule.weekend_start_time = weekend_start_time
        schedule.weekend_end_time = weekend_end_time
        
        return await self.schedule_crud.update_schedule(schedule)
        

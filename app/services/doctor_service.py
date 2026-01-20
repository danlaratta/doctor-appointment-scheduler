from datetime import date
from app.crud.doctor_crud import DoctorCrud
from app.models.doctor import Doctor

class DoctorService:
    def __init__(self, doctor_crud: DoctorCrud) -> None:
        self.doctor_crud = doctor_crud

    # Register new doctor
    async def register_new_doctor(self, fname: str, lname: str, dob: date, email: str, phone: str) -> Doctor:
        # Check if doctor already exists
        exists: bool = await self.doctor_crud.check_doctor_exists(email)

        if exists:
            raise ValueError('Cannot register doctor, doctor already exists')
        
        # Register doctor
        doctor: Doctor = Doctor(
            first_name = fname,
            last_name = lname,
            date_of_birth = dob,
            email = email,
            phone = phone,
        )

        return await self.doctor_crud.create_doctor(doctor)
from datetime import date
from app.crud.patient_crud import PatientCrud
from app.models.patient import Patient

class PatientService:
    def __init__(self, patient_crud: PatientCrud) -> None:
        self.patient_crud = patient_crud

    # Register new patient
    async def register_new_patient(self, fname: str, lname: str, dob: date, email: str, phone: str) -> Patient:
        # Check if patient already exists
        exists: bool = await self.patient_crud.check_patient_exists(email)

        if exists:
            raise ValueError('Cannot register patient, patient already exists')
        
        # Register patient
        patient: Patient = Patient(
            first_name = fname,
            last_name = lname,
            date_of_birth = dob,
            email = email,
            phone = phone,
        )

        return await self.patient_crud.create_patient(patient)